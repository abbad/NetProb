'''
Created on July 9, 2013

@author: Abbad

This module has function related to unnamed pipes

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
def sendMessage(message, pipe):
	# open pipe
	pipeoutfd = getOsFileHandle(pipe, O_WRONLY)
	
	# Read from pipe
	# Note:  Could be done with os.read/os.close directly, instead of os.fdopen
	pipeout = fdopen(pipeoutfd, 'w')
	pipeout.write(message)
	pipeout.close()
 
	
'''
	this function will pepare pipe
'''
def getOsFileHandle(pipe, flags):
	# Get file descriptor from argument
	pipe = int(pipe)
	if platform == "win32": # windows
		pipeoutfd = open_osfhandle(pipe, flags)
	else: # linux
		pipeoutfd = pipe
	
	return pipeoutfd
	

def getHandleDuplicate(pipe):
	'''
	This function will get you the duplicate the handle.
	'''
	if platform == "win32": # windows
		curproc = GetCurrentProcess()
		pipeHandle = get_osfhandle(pipe)
		pipeDuplicate = DuplicateHandle(curproc, pipeHandle, curproc, 0, 1,
				DUPLICATE_SAME_ACCESS)

		return pipeDuplicate
		
	else: # linux
		pipearg = str(pipe)
		
		return pipearg


def closePipe(pipe, pipeDuplicate):
	'''
		This will close the pipe end.
	'''
	close(pipe)
	if platform == "win32":
		pipeDuplicate.Close()
		
