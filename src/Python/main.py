'''
Created on may 7, 2013

@author: Abbad

This module will call UDP server and TCP server.

'''

from subprocess import Popen
from time import sleep
from msvcrt import getch
import os

def getch():
	import sys, tty, termios
	fd = sys.stdin.fileno()
	old = termios.tcgetattr(fd)
	try:
		tty.setraw(fd)
		return sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old)

if __name__ == '__main__':
	
	print 'Starting TCP server'
	args = ["python", "TCP\TCPserver.py"]
	p1 = Popen(args, shell=False)
	
	print 'Starting UDP server'
	args =  ["python", "UDP\UDPserver.py"]
	p2 = Popen(args, shell=False)
	
	print 'press any key to continue'
	
	try:
		os.system('pause')  #windows, doesn't require enter
	except ValueError:
		os.system('read -p "Press any key to continue"') #linux
	
	p1.terminate()
	p2.terminate()
	