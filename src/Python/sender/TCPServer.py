'''
Created on Apr 28, 2013

@author: Abbad
'''

from socket import socket, AF_INET, SOCK_STREAM
from sys import exit, argv
from getopt import getopt, GetoptError
from os import path as osPath
from inspect import currentframe, getfile
from sys import path

host = '127.0.0.1'
bufferSize = 4096 
port = 5005
notificationPeriod = 5
pipeArg = None

# code to include subfolder modules (packages)
cmd_subfolder = osPath.realpath(osPath.abspath(osPath.join(osPath.split(getfile(currentframe()))[0],"subfolder")))
if cmd_subfolder not in path:
	path.insert(0, cmd_subfolder)

from utilities.user_pipes import sendMessage	
from utilities.tcp_server_win32_named_pipes import *

def printHelp():
	print 'This is a TCP Server:'
	print 'usage:'
	print '-p port number \t\t\t default 5005'
	print '-n notification period'
	
def checkArguments(argv):
	try:
		opts, args = getopt(argv[1:],"hp:n:a:",["portNumber", "notificationPeriod", "pipeArg"])
	except GetoptError:
		print 'TCPServer.py -p <port> -n <notification period> -a <pipeArg>'
		exit(2)
	for opt, arg in opts:
		if opt == '-h':
			printHelp()
			exit()
		elif opt in ('-p'):
			global port 
			port = int(arg)
		elif opt in ('-n'):
			global notificationPeriod
			notificationPeriod = int(arg)
		elif opt in ('-a'):
			global pipeArg
			pipeArg = int(arg)

'''
	Create tcp connection and accept a connection.
'''
def createConnection():
	s = socket(AF_INET, SOCK_STREAM)
	s.bind((host, port))
	print 'server is listening'
	s.listen(1)

	conn, addr = s.accept()
	print 'TCP Server: Connection address:', addr
	return conn
	
'''
	Send to udp client in order to analyze it. 
'''
def sendToReciever(data):
	writeToPipe(data)
	

def main():
	global bufferSize
	checkArguments(argv)
	conn = createConnection()
	sendNotificationPeriod(conn)
	data = receiveConfirm(conn)
	
	# getting the confirm from receiver to start sending. 
	
	if data == "confirm":
		sendMessage("startUdpClient", pipeArg)
		
	while 1:
		data = conn.recv(bufferSize)
		sendToReciever(data)
	
	conn.close()

'''
	this function will send the notification period to client.
'''
def sendNotificationPeriod(conn):
	conn.sendall(str(notificationPeriod))

'''
	this function to receive confirm from the client. 
'''
def receiveConfirm(conn):
	return conn.recv(bufferSize)
	
if __name__ == '__main__':
	main()
	
