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

GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
PIPE_READMODE_MESSAGE = 0x2
OPEN_EXISTING = 0x3
INVALID_HANDLE_VALUE = -1
ERROR_PIPE_BUSY = 231
ERROR_MORE_DATA = 234
BUFSIZE = 512

szPipename = "\\\\.\\pipe\\mynamedpipe"

'''
	This function will write to named pipe.
'''
def writeToPipe(data):
    while 1:
		#create named pipe
		hPipe = windll.kernel32.CreateFileA(szPipename, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, None)
        # if  error break
		if (hPipe != INVALID_HANDLE_VALUE):
			break
		else:
			print "Invalid Handle Value"
		if (windll.kernel32.GetLastError() != ERROR_PIPE_BUSY):
			print "Could not open pipe"
			return
		elif ((windll.kernel32.WaitNamedPipeA(szPipename, 20000)) == 0):
			print "Could not open pipe\n"
			return


    dwMode = c_ulong(PIPE_READMODE_MESSAGE)
    fSuccess = windll.kernel32.SetNamedPipeHandleState(hPipe, byref(dwMode), None, None);
    if (not fSuccess):
        print "SetNamedPipeHandleState failed"
    cbWritten = c_ulong(0)
    fSuccess = windll.kernel32.WriteFile(hPipe, c_char_p(data), len(data), byref(cbWritten), None)
    if ((not fSuccess) or (len(data) != cbWritten.value)):
        print "Write File failed"
        return
    else:
		pass
        #print "Number of bytes written:", cbWritten.value

		'''
	fSuccess = 0
	chBuf = create_string_buffer(BUFSIZE)
	cbRead = c_ulong(0)
	while (not fSuccess): # repeat loop if ERROR_MORE_DATA
		fSuccess = windll.kernel32.ReadFile(hPipe, chBuf, BUFSIZE, byref(cbRead), None)
		if (fSuccess == 1):
			print "Number of bytes read:", cbRead.value
			print chBuf.value
			break
		elif (windll.kernel32.GetLastError() != ERROR_MORE_DATA):
			break
			'''
    windll.kernel32.CloseHandle(hPipe)
    return
    
    
if __name__ == "__main__":
    writeToPipe("12322")