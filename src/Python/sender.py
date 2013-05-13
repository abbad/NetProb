'''
Created on may 10, 2013

@author: Abbad

Sender Module to run the sender.

'''

from subprocess import Popen
from time import sleep
import os

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

def menu():
	
	p1 = None
	p2 = None
	
	while 1:
		print "Select one of the following:"
		print "1. start TCP Server"
		print "2. start UDP Client"
		print "3. quit"
		getch = _Getch() 
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