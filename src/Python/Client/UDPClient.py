'''
Created on Apr 13, 2013

@author: Abbad
'''

import socket
import os
import sys, getopt
import time

# global variables 
host = "localhost"
port = 4001
windowSize = 10
packetSize = 1000
duration = 10
timeBetweenPackets = 0 
numberOfPackets = 1

def sendUdpBasedOntime(sock):
	'''
		sending packets based on duration
	'''
	startTime = time.time()
	stopTime = startTime + duration
	print 'sending packets for about ' + str(duration) + ' of seconds'
	global numberOfPackets
	numberOfPackets = 1
		
	while(1):
			
		counter =0 
			
		for i in range(windowSize):
		
			packet = makePacket(packetSize, numberOfPackets)
			print 'sending packet', numberOfPackets 
			sock.sendto(packet , (host, port))
			numberOfPackets = numberOfPackets + 1
			
		print 'sleeping for ' + str(timeBetweenPackets) + ' seconds' 
		time.sleep(timeBetweenPackets)
		
		if stopTime <= time.time():
			print 'done'
			break
			
		

def printHelp():
	print 'This is a UDP client:'
	print 'usage:'
	print '-l localHost \t\t\t default localhost'
	print '-p port number \t\t\t default 4001'
	print '-s packet size \t\t\t default 50'
	print '-t time between each packet \t default 0 seconds'
	print '-w window size \t\t\t default 0'
	
def makePacket(size, number):

	packetheader = makePacketHeader( "packet number %d" % number)
	packetData = makePacketBody(size)
	
	return packetheader + packetData 
	
def makePacketHeader(header):
	return header 
	
def makePacketBody(size):
	return os.urandom(size)
	
def checkArguments(argv):
	try:
		opts, args = getopt.getopt(argv[1:],"hl:p:w:s:d:t:b:",["host", "portNumber", "numberOfPackets", "packetSize", "duration", "Time"])
	except getopt.GetoptError:
		print 'UDPClient.py -l <hostname> -p <port> -s <packetSize> -w windowSize -d <windowSize> -t <timeBetweenPackets>'
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
		elif opt in ('-s'):
			global packetSize
			packetSize = int(arg)
		elif opt in ('-w'):
			global windowSize
			windowSize = int(arg)
		elif opt in ('-d'):
			global duration
			duration = int(arg)
		elif opt in ('-t'):
			global timeBetweenPackets
			timeBetweenPackets = float(arg)
		
if __name__ == '__main__':
	print 'UDP target IP:', socket.gethostbyname(host)
	print 'UDP target port:', port
	
	checkArguments(sys.argv)
	
	sock = socket.socket(socket.AF_INET, # Internet
						             socket.SOCK_DGRAM) # UDP
	
	
	
	sendUdpBasedOntime(sock)
	
	# report 
	# tcp  
	
	print "Number of packets sent:", numberOfPackets
	
	print 'closing sockets'
	sock.close()
	