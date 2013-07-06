'''
Created on Apr 28, 2013

@author: Abbad
'''

import socket
import sys, getopt 

host = '127.0.0.1'
port = 5005
bufferSize = 1024 
notificationPeriod = 5

# global variables

def printHelp():
	print 'This is a TCP Server:'
	print 'usage:'
	print '-p port number \t\t\t default 5005'
	print '-n notification period'
	
def checkArguments(argv):
	try:
		opts, args = getopt.getopt(argv[1:],"hp:n:",["portNumber", "notificationPeriod"])
	except getopt.GetoptError:
		print 'TCPServer.py -p <port> -n <notification period>'
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

def createConnection():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	print 'server is listening'
	s.listen(1)

	conn, addr = s.accept()
	print 'TCP Server: Connection address:', addr
	return conn

'''
	this function will send the notification period to client.
'''
def sendNotificationPeriod(conn):
	conn.sendall("<notificationPeriod>"+ str(notificationPeriod) +"</notificationPeriod>")

def main():
	checkArguments(sys.argv)
	conn = createConnection()
	sendNotificationPeriod(conn)
	
	while 1:
		data = conn.recv(bufferSize)
		print "TCP Server: received data:", data
		conn.close()
	
if __name__ == '__main__':
	
	main()
	
