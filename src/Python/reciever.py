'''
Created on may 7, 2013

@author: Abbad

This module will call UDP server and TCP server.

'''

from subprocess import Popen
from time import sleep
import os

if __name__ == '__main__':
	
	print 'Starting TCP server'
	args = ["python", "TCP\TCPClient.py"]
	p1 = Popen(args, shell=False)
	
	print 'Starting UDP server'
	args =  ["python", "UDP\UDPserver.py"]
	p2 = Popen(args, shell=False)
	
	try:
		os.system('pause')  #windows, doesn't require enter
	except ValueError:
		os.system('read -p "Press any key to continue"') #linux
	
	p1.terminate()
	p2.terminate()
	