'''
Created on Apr 28, 2013

@author: Abbad
'''

import socket
import sys, getopt 
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

from utilities.user_pipes import notifyParent	


def printHelp():
	print 'This is a TCP Server:'
	print 'usage:'
	print '-p port number \t\t\t default 5005'
	print '-n notification period'
	
def checkArguments(argv):
	try:
		opts, args = getopt.getopt(argv[1:],"hp:n:a:",["portNumber", "notificationPeriod", "pipeArg"])
	except getopt.GetoptError:
		print 'TCPServer.py -p <port> -n <notification period> -a <pipeArg>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			printHelp()
			sys.exit()
		elif opt in ('-p'):
			global port 
			port = int(arg)
		elif opt in ('-n'):
			global notificationPeriod
			notificationPeriod = int(arg)
		elif opt in ('-a'):
			global pipeArg
			pipeArg = int(arg)

def createConnection():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	print 'server is listening'
	s.listen(1)

	conn, addr = s.accept()
	print 'TCP Server: Connection address:', addr
	return conn

def main():
	global bufferSize
	checkArguments(sys.argv)
	conn = createConnection()
	sendNotificationPeriod(conn)
	data = receiveConfirm(conn)
	print data
	if data == "confirm":
		notifyParent("startUdpClient", pipeArg)
	'''
	while 1:
	
		data = conn.recv(bufferSize)
		print "TCP Server: received data:", data
		conn.close()'''

'''
	this function will send the notification period to client.
'''
def sendNotificationPeriod(conn):
	conn.sendall("<notificationPeriod>" + str(notificationPeriod) + "</notificationPeriod>")

'''
	this function to receive confirm from the client. 
'''
def receiveConfirm(conn):
	return conn.recv(bufferSize)
	
	
if __name__ == '__main__':
	
	main()
	
