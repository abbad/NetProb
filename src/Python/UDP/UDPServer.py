'''
Created on Apr 13, 2013

@author: Abbad
'''

import socket
import sys, getopt
import time
from time import strftime
from interpreter import getPacketSequenceNumber
import thread

# global variables
host = "localhost"              # Symbolic name meaning all available interfaces
port = 4001                     # Arbitrary non-privileged port
bufferSize = 2084
statNotPeriod = 20 				#statisticsNotificationPeriod. // this means that the server will drop a statistics 
fileName = "statistics "
numberOfPackets = 0
	
def writeStatistics():
	'''
		this is to write statistics to a file.
	'''
	with open(fileName +  strftime("%H%M%S") + '.xml', 'w') as f:
		f.write(__generateStatistics())
	
	f.close()
	
def __generateStatistics():
	'''
		A function to generate xml statistics for server.
	'''
	return '''<updStatistics><packetsSend>''' + str(numberOfPackets) + '''</packetsSend></updStatistics> '''
	 
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
		opts, args = getopt.getopt(argv[1:],"hl:p:b:f:n:",["host", "portNumber", "bufferSize", "fileName", "notificationPeriod", "peerPID"])
	except getopt.GetoptError:
		print 'UDPServer.py -l <hostname> -p <port> -b <bufferSize> -f <fileName> -n <notificationPeriod>'
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
		elif opt in ('-f'):
			global fileName
			fileName = arg
		elif opt in ('-n'):
			global statNotPeriod
			statNotPeriod = int(arg)
		
if __name__ == "__main__":

	checkArguments(sys.argv)
	
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	sock.bind((host, port))

	startTime = time.time()
	stopTime = startTime + statNotPeriod
	
	print "Server is listening.."
	
	while 1:
		data  = sock.recv(bufferSize)
		print "received message:\nsize:" + str(len(data))
		
		numberOfPackets += 1
	
		if stopTime <= time.time():
			print 'writing statistics'
			thread.start_new_thread(writeStatistics, ())
			startTime = time.time()
			stopTime = startTime + statNotPeriod
				
