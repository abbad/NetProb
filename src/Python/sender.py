'''
Created on may 10, 2013

@author: Abbad

Module to run the sender.

'''

from subprocess import Popen
import os
from inspect import currentframe, getfile
from sys import path
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(getfile( currentframe() ))[0],"subfolder")))
if cmd_subfolder not in path:
	path.insert(0, cmd_subfolder)

from utilities.getChar import *

def menu():
	
	p1 = None
	p2 = None
	
	while 1:
		print "Select one of the following:"
		print "1. start TCP Server"
		print "2. start UDP Client"
		print "3. quit"
		getch = Getch() 
		val = getch.__call__()
		if val == '1':
			p1 = launchTCPServer()
		if val == '2':
			p2 = launchUdpClient()
		if val == '3':
			try:
				if p1:
					p1.terminate()
				if p2:
					p2.terminate()
			except:
				print "error while terminating one of the processes"
			exit()

def launchTCPServer():
	print 'Starting TCP server'
	args = ["python", "TCP\TCPServer.py"]
	return(Popen(args, shell=False))
	
	
def launchUdpClient():
	print 'Starting UDP client'
	args =  ["python", "UDP\UDPClient.py", "-d 400"]
	return(Popen(args, shell=False))

if __name__ == '__main__':
	 
	menu()
	
	'''
	
	try:
		os.system('pause')  #windows, doesn't require enter
	except ValueError:
		os.system('read -p "Press any key to continue"') #linux
	
	try:
		p1.terminate()
		p2.terminate()
	except:
		pass
	'''