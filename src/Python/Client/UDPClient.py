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
	counter = 1 
	
	while(1):
		packetHeader = "packet number %d" % counter
		packetData = os.urandom(packetSize)
		print 'sending'+ packetHeader
		time.sleep(timeBetweenPackets)
		sock.sendto(packetHeader + packetData , (host, port))
		counter = counter + 1
		if stopTime <= time.time():
			print 'done'
			break


def sendUdpBasedOnPackets(sock):
	'''
		sending packets based on number of packets 
	'''	
	for x in range (0,numberOfPackets):
		
		packet = x + 1
		packetHeader = "packet number %d" % packet
		packetData = os.urandom(packetSize)
		print 'sending'+ packetHeader
		time.sleep(timeBetweenPackets)
		sock.sendto(packetHeader + packetData , (host, port))
	
	print "Number of packets sent:", numberOfPackets
	
	
def printHelp():
	print 'This is a UDP client:'
	print 'usage:'
	print '-l localHost \t\t\t default localhost'
	print '-p port number \t\t\t default 4001'
	print '-s packet size \t\t\t default 50'
	print '-n number of packets \t\t default 1000'
	print '-d duration sending packets \t default 10 seconds'
	print '-t time between each packet \t default 0 seconds'
	
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
			global localHost
			localHost = arg
		elif opt in ('-p'):
			global port 
			port = int(arg)
		elif opt in ('-s'):
			global packetSize
			packetSize = arg
		elif opt in ('-n'):
			global numberOfPackets
			numberOfPackets = arg
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
		print 'sending packets for about %d of seconds', duration
		sendUdpBasedOntime(sock)
	else: 
		print 'Number of packets:', numberOfPackets
		sendUdpBasedOnPackets(sock)
	
	print 'closing sockets'
	sock.close()
	