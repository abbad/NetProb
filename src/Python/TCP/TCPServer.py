'''
Created on Apr 28, 2013

@author: Abbad
'''

import socket
import sys, getopt 

host = '127.0.0.1'
port = 5005
bufferSize = 1024 

# global variables

def printHelp():
	print 'This is a TCP Server:'
	print 'usage:'
	print '-l localHost \t\t\t default localhost'
	print '-p port number \t\t\t default 5005'
	print '-s buffer size \t\t\t default 1024'

def checkArguments(argv):
	try:
		opts, args = getopt.getopt(argv[1:],"hl:p:s:",["host", "portNumber", "bufferSize"])
	except getopt.GetoptError:
		print 'TCPServer.py -l <hostname> -p <port> -s <bufferSize>'
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
		elif opt in ('-b'):
			global bufferSize
			bufferSize = int(arg)

   
checkArguments(sys.argv)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
print 'server is listening'
s.listen(1)


conn, addr = s.accept()
print 'TCP Server: Connection address:', addr

while 1:
	data = conn.recv(bufferSize)
	print "TCP Server: received data:", data

	
conn.close()