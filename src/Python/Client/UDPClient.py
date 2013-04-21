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
numberOfPackets = 10
packetSize = 1000
duration = 10
timeBetweenPackets = 0 
timeBased = False 

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
		packet = makePacket(packetSize, numberOfPackets)
		print 'sending packet', numberOfPackets 
		
		time.sleep(timeBetweenPackets)
		sock.sendto(packet , (host, port))
		
		if stopTime <= time.time():
			print 'done'
			break
			
		numberOfPackets = numberOfPackets + 1

def sendUdpBasedOnPackets(sock):
	'''
		sending packets based on number of packets 
	'''	
	for x in range (0,numberOfPackets):
		counter = x+1 
		print 'sending packet number '+ str(counter)
		packet = makePacket(packetSize, counter)
		time.sleep(timeBetweenPackets)
		sock.sendto(packet, (host, port))
		
def printHelp():
	print 'This is a UDP client:'
	print 'usage:'
	print '-l localHost \t\t\t default localhost'
	print '-p port number \t\t\t default 4001'
	print '-s packet size \t\t\t default 50'
	print '-n number of packets \t\t default 1000' # remove 
	print '-d duration sending packets \t default 10 seconds'
	print '-t time between each packet \t default 0 seconds'
	print 'note: option -d will override option -n.'
	print '-w window size'
	
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
		opts, args = getopt.getopt(argv[1:],"hl:p:n:s:d:t:b:",["host", "portNumber", "numberOfPackets", "packetSize", "duration", "Time"])
	except getopt.GetoptError:
		print 'UDPClient.py -l <hostname> -p <port> -s <packetSize> -n <numberOfPackets> -d <duration> -t <timeBetweenPackets>'
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
		elif opt in ('-n'):
			global numberOfPackets
			numberOfPackets = int(arg)
		elif opt in ('-d'):
			global duration 
			global timeBased
			duration = int(arg)
			timeBased = True
		elif opt in ('-t'):
			global timeBetweenPackets
			timeBetweenPackets = float(arg)
		
if __name__ == '__main__':
	print 'UDP target IP:', socket.gethostbyname(host)
	print 'UDP target port:', port
	
	checkArguments(sys.argv)
	
	sock = socket.socket(socket.AF_INET, # Internet
						             socket.SOCK_DGRAM) # UDP
	
	
	if timeBased:
		sendUdpBasedOntime(sock)
	else: 
		sendUdpBasedOnPackets(sock)
	
	print "Number of packets sent:", numberOfPackets
	
	print 'closing sockets'
	sock.close()
	