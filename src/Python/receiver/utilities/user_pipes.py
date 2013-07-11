'''
Created on July 9, 2013

@author: Abbad

This module has all functions related to pipes.

'''

from os import O_WRONLY, fdopen, close, write, read
from sys import platform

if platform == "win32":
    from msvcrt import open_osfhandle, get_osfhandle

if platform == "win32":
	from _subprocess import GetCurrentProcess, DuplicateHandle, DUPLICATE_SAME_ACCESS
else:
	from fcntl import fcntl

	
'''
	using pipes a message to parent is sent to start udp server. 
'''	
def notifyParent(message, pipe):
	# open pipe
	pipeoutfd = openPipe(pipe, O_WRONLY )
	
	# Read from pipe
	# Note:  Could be done with os.read/os.close directly, instead of os.fdopen
	pipeout = fdopen(pipeoutfd, 'w')
	pipeout.write(message)
	pipeout.close()
 
	
'''
	this function will pepare pipe
'''
def openPipe(pipe ,flags):
	# Get file descriptor from argument
	pipe = int(pipe)
	if platform == "win32": # windows
		pipeoutfd = open_osfhandle(pipe, flags)
	else: # linux
		pipeoutfd = pipe
	
	return pipeoutfd
	
'''
		This function will prepare the pipe before passing it to a subprocess, because of a file descriptor inheritance issue in windows. 
'''
def preparePipes(pipe, pipeToClose):

	# Prepare to pass to child process
	if platform == "win32": # windows
		curproc = GetCurrentProcess()
		pipeHandle = get_osfhandle(pipe)
		pipeDuplicate = DuplicateHandle(curproc, pipeHandle, curproc, 0, 1,
				DUPLICATE_SAME_ACCESS)

		return str(int(pipeDuplicate)), pipeDuplicate
		
	else: # linux
		pipearg = str(pipe)

		# Must close pipe input if child will block waiting for end
		# Can also be closed in a preexec_fn passed to subprocess.Popen
		fcntl(pipeToClose, fcntl.F_SETFD, fcntl.FD_CLOEXEC)
		
		return pipearg

'''
	This will close the pipe end.
'''
def closePipe(pipe, pipeHandler):
	close(pipe)
	if platform == "win32":
		pipeHandler.Close()
		
