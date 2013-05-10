'''
Created on may 7, 2013

@author: Abbad

This module will call UDP server and TCP server.

'''

from subprocess import Popen, PIPE
from time import sleep
from os import system, path, pipe, fdopen

def get_reader_writer():
    fd_read, fd_write = pipe()
    return fdopen(fd_read, 'r'), fdopen(fd_write, 'w')

if __name__ == '__main__':
	
	# init reader and writer. 
	reader, writer = get_reader_writer()
	
	print 'Starting TCP client'
	args = ["python", "TCP\TCPClient.py"]
	p1 = Popen(args, stdin= PIPE, stdout= PIPE, shell=False)
	
	print 'Starting UDP server'
	args =  ["python", "UDP\UDPserver.py", "-n 5"]
	p2 = Popen(args, stdin= PIPE, stdout= PIPE, shell=False)
	
	try:
		system('pause')  #windows, doesn't require enter
	except ValueError:
		system('read -p "Press any key to continue"') #linux
	
	try:
		p1.terminate()
		p2.terminate()
	except:
		pass
		