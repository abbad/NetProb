'''
Created on Apr 29, 2013

@author: Abbad
'''

import socket
import os
import sys, getopt
import time

# global variables 
host = "localhost"
port = 5005

def printHelp():
	'''
		this is to print options.
	'''
	
	print 'This is a TCP client:'
	print 'usage:'
	print '-l localHost \t\t\t default localhost'
	print '-p port number \t\t\t default 5005'
	
def checkArguments(argv):
	'''
		this is to check arguments.
	'''
	try:
		opts, args = getopt.getopt(argv[1:], "hl:p:", ["host", "portNumber"])
	except getopt.GetoptError:
		print 'TCPClient.py -l <hostname> -p <port>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			printHelp()
			sys.exit()
		elif opt in ('-l'):
			global host
			host = arg
		elif opt in ('-p'):
			global port
			port = int(arg)

def getFileName():
	'''
		using listdir function in os to find files ending with
		xml if one found then return it to function.
	'''
	
	while 1:
		for files in os.listdir("."):
			if files.endswith(".xml"):
				return files
	
def deleteStatistics(fileName):
	os.remove(fileName)
	
	
def getStatistics():
	'''
		this is to open and read the statistics which are dumped from udp server. once read are also deleted.
	'''
	
	fileName = getFileName()
	with open(fileName,'r') as f:
		read_data = f.read()
	
	f.close()
	deleteStatistics(fileName)
	print read_data
	return read_data 
	
if __name__ == '__main__':
	'''
		start of the program.
	'''
	
	checkArguments(sys.argv)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	while 1:
		try:
			s.connect((host, port))
			print 'TCP Client: Connection established.'
			break
		except: 
			sleepTime = 5
			print 'TCP Client: sleeping for ' + str(sleepTime) + ' seconds'
			time.sleep(sleepTime)
		
		
	while 1:
		time.sleep(2)
		s.send(getStatistics())
		
	
	s.close()
	