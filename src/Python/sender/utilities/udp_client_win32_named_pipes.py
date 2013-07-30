'''
	This module used in sending data between tcp server and udp client. 
	Copied from the internet and modified. 
	
	Hello,
	Here is an example of Multithreaded Pipe Server and Client using the
		excellent ctypes library (Windows).

	Reference - MSDN:
	http://msdn.microsoft.com/library/default.asp?url=/library/en-us/ipc/base/multithreaded_pipe_server.asp
	and
	http://msdn.microsoft.com/library/default.asp?url=/library/en-us/ipc/base/named_pipe_client.asp

	Best Regards,
	Srijit
'''

from ctypes import *
from UDPServer import packetsRecievedQueue

PIPE_ACCESS_DUPLEX = 0x3
PIPE_TYPE_MESSAGE = 0x4
PIPE_READMODE_MESSAGE = 0x2
PIPE_WAIT = 0
PIPE_UNLIMITED_INSTANCES = 255
BUFSIZE = 4096
NMPWAIT_USE_DEFAULT_WAIT = 0
INVALID_HANDLE_VALUE = -1
ERROR_PIPE_CONNECTED = 535



MESSAGE = "Default message from client\0"
szPipename = "\\\\.\\pipe\\mynamedpipe"

'''
	Creates an instance of a named pipe and returns a 
	handle for subsequent pipe operations. A named pipe 
	server process uses this function either to create 
	the first instance of a specific named pipe and 
	establish its basic attributes or to create a 
	new instance of an existing named pipe.
'''

def createNamedPipe():
	# create
	hPipe = windll.kernel32.CreateNamedPipeA(szPipename,
                                                 PIPE_ACCESS_DUPLEX,
                                                 PIPE_TYPE_MESSAGE |
                                                 PIPE_READMODE_MESSAGE|
                                                 PIPE_WAIT, PIPE_UNLIMITED_INSTANCES,
                                                 BUFSIZE, BUFSIZE, NMPWAIT_USE_DEFAULT_WAIT,
                                                 None
                                                )
	
	# check for errors					
	if (hPipe == INVALID_HANDLE_VALUE):
		print "Error in creating Named Pipe"
		return 0
	
	return hPipe
		
'''
	Enables a named pipe server process to 
	wait for a client process to connect to 
	an instance of a named pipe. 
	A client process connects by calling either 
	the CreateFile or CallNamedPipe function.
'''
def connectToPipe(hPipe):

	fConnected = windll.kernel32.ConnectNamedPipe(hPipe, None)
	if ((fConnected == 0) and (windll.kernel32.GetLastError() == ERROR_PIPE_CONNECTED)):
		fConnected = 1
	if (fConnected == 1):
		return 1
	else:
		print "Could not connect to the Named Pipe"
		windll.kernel32.CloseHandle(hPipe)

'''
	Creates a thread to execute within the virtual address space of the calling process.
	To create a thread that runs in the virtual address space of another process, use the CreateRemoteThread function.
'''	
def createThread(hPipe, thread_func):
	dwThreadId = c_ulong(0)
	hThread = windll.kernel32.CreateThread(None, 0, thread_func, hPipe, 0, byref(dwThreadId))
	if (hThread == -1):
		print "Create Thread failed"
		return 0
	else:
		windll.kernel32.CloseHandle(hThread)

'''
	This function will just will read the value from the pipe.
'''
def ReadWrite_ClientPipe_Thread(hPipe):
    chBuf = create_string_buffer(BUFSIZE)
    cbRead = c_ulong(0)
    while 1:
        fSuccess = windll.kernel32.ReadFile(hPipe, chBuf, BUFSIZE,byref(cbRead), None)
        if ((fSuccess ==1) or (cbRead.value != 0)):
			packetsRecievedQueue.put(int(chBuf.value))
			print chBuf.value
			cbWritten = c_ulong(0)
			'''fSuccess = windll.kernel32.WriteFile(hPipe,
                                                 c_char_p(MESSAGE),
                                                 len(MESSAGE),
                                                 byref(cbWritten),
                                                 None
                                                )
			'''
        else:
            break
			
    windll.kernel32.FlushFileBuffers(hPipe)
    windll.kernel32.DisconnectNamedPipe(hPipe)
    windll.kernel32.CloseHandle(hPipe)
    return 0
	
def readFromPipe():
	
	THREADFUNC = CFUNCTYPE(c_int, c_int)
	thread_func = THREADFUNC(ReadWrite_ClientPipe_Thread)
	while 1:
		pipe = createNamedPipe()
		
		if (connectToPipe(pipe) == 1):
			createThread(pipe, thread_func)

	
if __name__ == '__main__':
	readFromPipe()