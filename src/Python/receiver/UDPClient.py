'''
Created on Apr 13, 2013

@author: Abbad
'''

from socket import socket, AF_INET, SOCK_DGRAM
from sys import platform, exit, argv
from getopt import getopt, GetoptError
from time import time, sleep
from thread import start_new_thread
from os import write

from utilities.udp_client_win32_named_pipes import writeToPipe

# global variables
host = "192.168.0.1"              # Symbolic name meaning all available interfaces
port = 4001                     # Arbitrary non-privileged port
bufferSize = 2084
statNotPeriod = 20 				#statisticsNotificationPeriod. // this means that the server will drop a statistics 
numberOfPackets = 0
pipeIn = None
	
	
def __generateStatistics(packets):
	'''
		A function to generate xml statistics for client.
	'''
	return str(packets)
	 
def printHelp():
	print 'This is a UDP client:'
	print 'usage:'
	print '-l localHost \t\t\t default localhost'
	print '-p port number \t\t\t default 4001'
	print '-b buffer size \t\t\t default 1024'
	print '-f file name \t\t\t default stat.xml'
	print '-n notification period \t\t default 20 seconds'

def checkArguments(argv):
	try:
		opts, args = getopt(argv[1:],"hl:p:b:n:",["host", "portNumber", "bufferSize", "notificationPeriod"])
	except GetoptError:
		print 'UDPClient .py -l <hostname> -p <port> -b <bufferSize> -n <notificationPeriod>'
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
		elif opt in ('-n'):
			global statNotPeriod
			statNotPeriod = int(arg)

def monitorValues():
	'''
		this function will keep on checking on the notificatin peroid. 
	'''	
	global numberOfPackets
	startTime = time()
	stopTime = startTime + statNotPeriod
	while 1:
		if stopTime <= time():
			start_new_thread(writeToPipe, ( str(numberOfPackets) + "time:" + str(time()),))
			stopTime = time() + statNotPeriod
			numberOfPackets = 0
		
if __name__ == "__main__":
		
	checkArguments(argv)
	
	sock = socket(AF_INET, SOCK_DGRAM)
	#sock.setblocking(0)
	sock.bind((host, port))
	print host
	print "UDP Client : Client  is listening.."
	start_new_thread(monitorValues, ())
	
	while 1:
		try:
			data  = sock.recv(bufferSize)
			print "UDP Client : received message " + str(numberOfPackets)
			#print "UDP Client : size:" + str(len(data))
			numberOfPackets += 1
		except: 
			pass
		
		
