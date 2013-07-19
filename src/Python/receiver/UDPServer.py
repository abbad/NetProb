'''
Created on Apr 13, 2013

@author: Abbad
'''

from socket import socket, AF_INET, SOCK_DGRAM
from sys import platform, exit, argv
from getopt import getopt, GetoptError
from time import strftime, time, sleep
from thread import start_new_thread
from os import write

from utilities.udp_server_win32_named_pipes import writeToPipe

# global variables
host = "192.168.0.1"              # Symbolic name meaning all available interfaces
port = 4001                     # Arbitrary non-privileged port
bufferSize = 2084
statNotPeriod = 20 				#statisticsNotificationPeriod. // this means that the server will drop a statistics 
fileName = "statistics "
numberOfPackets = 0
pipeIn = None

def writeStatistics(packets):
	'''
		this is to write statistics to a file.
	'''
	with open(fileName +  strftime("%H%M%S") + '.xml', 'w') as f:
		f.write(__generateStatistics(packets))
	
	f.close()
	
	
def __generateStatistics(packets):
	'''
		A function to generate xml statistics for server.
	'''
	return str(packets)
	 
def printHelp():
	print 'This is a UDP Server:'
	print 'usage:'
	print '-l localHost \t\t\t default localhost'
	print '-p port number \t\t\t default 4001'
	print '-b buffer size \t\t\t default 1024'
	print '-f file name \t\t\t default stat.xml'
	print '-n notification period \t\t default 20 seconds'

def checkArguments(argv):
	try:
		opts, args = getopt(argv[1:],"hl:p:b:f:n:",["host", "portNumber", "bufferSize", "fileName", "notificationPeriod"])
	except GetoptError:
		print 'UDPServer.py -l <hostname> -p <port> -b <bufferSize> -f <fileName> -n <notificationPeriod>'
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
		elif opt in ('-b'):
			global bufferSize
			bufferSize = int(arg)
		elif opt in ('-f'):
			global fileName
			fileName = arg
		elif opt in ('-n'):
			global statNotPeriod
			statNotPeriod = int(arg)
		
if __name__ == "__main__":
		
	checkArguments(argv)
	
	sock = socket(AF_INET, SOCK_DGRAM)

	sock.bind((host, port))

	startTime = time()
	stopTime = startTime + statNotPeriod
	
	print "UDP Server: Server is listening.."
	
	while 1:
		data  = sock.recv(bufferSize)
		print "UDP Server: received message " + str(numberOfPackets)
		#print "UDP Server: size:" + str(len(data))
		
		numberOfPackets += 1
		
		if stopTime <= time():
			
			start_new_thread(writeToPipe, ( str(numberOfPackets),))
			startTime = time()
			stopTime = startTime + statNotPeriod
			numberOfPackets = 0