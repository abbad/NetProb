'''
Created on Apr 29, 2013

@author: Abbad
'''

import socket
import sys, getopt
from time import sleep
from os import read, listdir, remove
from os import path as osPath
from inspect import currentframe, getfile
from sys import path

if sys.platform == "win32":
    from msvcrt import open_osfhandle 

# global variables 
host = "localhost"
port = 5005
pipeArg1 = None

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
		opts, args = getopt.getopt(argv[1:], "hl:p:a:v:", ["host", "portNumber", "pipeArg1"])
	except getopt.GetoptError:
		print 'TCPClient.py -l <hostname> -p <port> -a <pipeArg1>'
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
			global pipeArg1 
			pipeArg1 = int(arg)
			
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
	remove(fileName)
	
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
	
	# read from tcp server.
	notificationPeriod = getNotificationPeriod(s)
	# notify the parent to launch the udp server with the notification period read from tcp server.
	notifyParent("startUdpServer" + notificationPeriod, pipeArg1)
	sendConfirm(s)
	
	
	while 1:
		stat = getStatistics()
		s.send(stat)
	'''
	while 1:
		try:

			break
		except: 
			sleepTime = 5
			print 'TCP Client: sleeping for ' + str(sleepTime) + ' seconds'
			sleep(sleepTime)
	'''
	
	#s.close()
	