'''
Created on Apr 29, 2013

@author: Abbad
'''

from socket import socket, AF_INET, SOCK_STREAM
from sys import exit, argv, path
from getopt import getopt, GetoptError
from time import sleep
from os import read, listdir, remove
from os import path as osPath
from inspect import currentframe, getfile
from thread import start_new_thread
from Queue import Queue

# global variables 
host = "localHost"
port = 5005
pipeArg1 = None
receivedMessagesQueue = Queue()

# code to include subfolder modules (packages)
cmd_subfolder = osPath.realpath(osPath.abspath(osPath.join(osPath.split(getfile(currentframe()))[0],"subfolder")))
if cmd_subfolder not in path:
	path.insert(0, cmd_subfolder)

from utilities.tcp_client_win32_named_pipes import *
from utilities.udp_tcp_client_unnamed_pipes import sendMessage

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
		opts, args = getopt(argv[1:], "hl:p:a:v:", ["host", "portNumber", "pipeArg1"])
	except GetoptError:
		print 'TCPClient.py -l <hostname> -p <port> -a <pipeArg1>'
		exit(2)
	for opt, arg in opts:
		if opt == '-h':
			printHelp()
			exit()
		elif opt in ('-l'):
			global host
			host = arg
		elif opt in ('-p'):
			global port
			port = int(arg)
		elif opt in ('-a'):
			global pipeArg1 
			pipeArg1 = int(arg)
			
		
def getNotificationPeriod(conn):
	'''
		This function to get notification period from server.
	'''
	return conn.recv(4096)
	

def sendConfirm(conn):
	'''
		This function to send confirm to server.
	'''
	conn.send("confirm")
	
if __name__ == '__main__':
	'''
		start of the program.
	'''
	
	checkArguments(argv)
	s = socket(AF_INET, SOCK_STREAM)
	while (1):
		try:
			s.connect((host, port))
			break
		except: 
			sleep(5)
	print 'TCP Client: Connection established.'
	
	# read from tcp server.
	notificationPeriod = getNotificationPeriod(s)
	# notify the parent to launch the udp server with the notification period read from tcp server.
	sendConfirm(s)
	sendMessage("startUdpClient" + notificationPeriod, pipeArg1)
	
	while 1:
		# start looking for statistics and send them to tcp server in sender. 
		start_new_thread(readFromPipe, ())
		message = str(receivedMessagesQueue.get())
		s.send(message)
		#stat = getStatistics() 
		#s.send(stat)
	
	s.close()
	