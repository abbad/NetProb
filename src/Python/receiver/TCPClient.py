'''
Created on Apr 29, 2013

@author: Abbad
'''

import socket
import sys, getopt
from time import sleep
from os import pipe, fdopen, read, listdir
from os import path as osPath
from inspect import currentframe, getfile
from sys import path

# global variables 
host = "localhost"
port = 5005
pipeArg = None

# code to include subfolder modules (packages)
cmd_subfolder = osPath.realpath(osPath.abspath(osPath.join(osPath.split(getfile(currentframe()))[0],"subfolder")))
if cmd_subfolder not in path:
	path.insert(0, cmd_subfolder)

from utilities.user_pipes import notifyParent

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
		opts, args = getopt.getopt(argv[1:], "hl:p:a:", ["host", "portNumber", "pipeArg"])
	except getopt.GetoptError:
		print 'TCPClient.py -l <hostname> -p <port> -a <pipeArg>'
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
		elif opt in ('-a'):
			global pipeArg 
			pipeArg = int(arg)
			
def getFileName():
	'''
		using listdir function in os to find files ending with
		xml if one found then return it to function.
	'''
	
	while 1:
		for files in listdir("."):
			if files.endswith(".xml"):
				return files
	
def deleteStatistics(fileName):
	os.remove(fileName)
	
	
def getStatistics():
	'''
		this is to open and read the statistics which are dumped from udp server. once read are also deleted.
	'''
	
	fileName = getFileName()
	with open(fileName, 'r') as f:
		sleep(1)
		read_data = f.read()
			
	f.close()
	deleteStatistics(fileName)
	return read_data 

'''
	This function to get notification period from server.
'''
def getNotificationPeriod(conn):
	return conn.recv(4096)
	#print 'TCP Client:' + data
	
'''
	This function to send confirm to server.
'''
def sendConfirm(conn):
	conn.send("confirm")
	
if __name__ == '__main__':
	'''
		start of the program.
	'''
	
	checkArguments(sys.argv)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	print 'TCP Client: Connection established.'
	notificationPeriod = getNotificationPeriod(s)
	notifyParent("startUdpServer"+notificationPeriod, pipeArg)
	sendConfirm(s)
	
	'''
	while 1:
		try:

			break
		except: 
			sleepTime = 5
			print 'TCP Client: sleeping for ' + str(sleepTime) + ' seconds'
			sleep(sleepTime)
		
		
	while 1:
		sleep(2)
		stat = getStatistics()
		s.send(stat)
		
	'''
	s.close()
	