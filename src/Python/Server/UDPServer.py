'''
Created on Apr 13, 2013

@author: Abbad
'''

import socket
import sys, getopt

# global variables
host = "localhost"              # Symbolic name meaning all available interfaces
port = 4001                     # Arbitrary non-privileged port

def printHelp():
	print 'This is a UDP client:'
	print 'usage:'
	print '-l localHost \t\t\t default localhost'
	print '-p port number \t\t\t default 4001'

def checkArguments(argv):
	try:
		opts, args = getopt.getopt(argv[1:],"hl:p:",["host", "portNumber"])
	except getopt.GetoptError:
		print 'UDPClient.py -l <hostname> -p <port> -s'
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

if __name__ == "__main__":
	checkArguments(sys.argv)

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	sock.bind((host, port))

	print "Server is listening.."

	while 1:
		data  = sock.recv(1024)
		print "received message:\nsize:" + str(len(data))
	
	