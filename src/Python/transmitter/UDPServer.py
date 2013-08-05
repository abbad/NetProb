'''
Created on Apr 13, 2013

@author: Abbad
'''

from __future__ import division
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
from os import urandom
from sys import exit, argv
from getopt import getopt, GetoptError
from time import sleep, time
from thread import start_new_thread
from os import path as osPath
from inspect import currentframe, getfile
from sys import path
from Queue import Queue, Empty
from threading import Thread 
from utilities.file_io import writeToLog, readInput, parseLine
from utilities.udp_server_win32_named_pipes import *
# code to include subfolder modules (packages)
#cmd_subfolder = osPath.realpath(osPath.abspath(osPath.join(osPath.split(getfile(currentframe()))[0],"subfolder")))
#if cmd_subfolder not in path:
# 	path.insert(0, cmd_subfolder)

# global variables 
host = "localhost"
port = 4001
PacketsPerWindows = 10
packetSize = 1000
duration = 10
timeBetweenWindows = 0 
numberOfPackets = 1
notificationPeriod = 0

# flags
nonUniform = False

def sendUdpBasedOnDuration(sock):
	'''
		sending packets based on duration
	'''
	startTime = time()
	stopDurationTime = startTime + duration
	totalNumberOfPacketsSend = 0
	print 'UDP Client: sending packets for about ' + str(duration) + ' of seconds'
	global numberOfPackets
	numberOfPackets = 0
	
	while(1):
		# send a window a loop
		for i in range(PacketsPerWindows):	
			packet = makePacket(packetSize, numberOfPackets)
			sock.sendto(packet , (host, port))
			numberOfPackets = numberOfPackets + 1
			totalNumberOfPacketsSend = totalNumberOfPacketsSend + 1
			
		if timeBetweenWindows != 0:
			print 'sleeping for ' + str(timeBetweenWindows) + ' seconds' 
			sleep(timeBetweenWindows)
		
		if stopDurationTime <= time():
			print 'done'
			break
			
	return totalNumberOfPacketsSend

def putValuesInQueue(startTime, packetsSendQueue, timeStampSendQueue):
	'''
		This function will put the values in the queue
	'''
	global numberOfPackets
	
	notificationTime = startTime + notificationPeriod
	
	while(1):
		if notificationTime <= time():
			packetsSendQueue.put(numberOfPackets)
			timeStampSendQueue.put(time())
			numberOfPackets = 0
			notificationTime = time() + notificationPeriod
		
			
def printHelp():
	print 'This is a UDP Server:'
	print 'usage:'
	print '-l localHost \t\t\t default localhost'
	print '-p port number \t\t\t default 4001'
	print '-s packet size \t\t\t default 50'
	print '-t time between each window \t default 0 seconds'
	print '-w window size \t\t\t default 0'
	print '-d duration sending packets \t dafault 20'
	print '-n notification period \t default 5 \n'
	
def makePacket(size, number):
	packetheader = makePacketHeader(number)
	packetData = makePacketBody(size)
	
	return packetheader + packetData 
	
def makePacketHeader(header):
	'''
		specification first 32 bits are reserved for squence number 
	'''
	return bytearray('{0:32b}'.format(header))

def makePacketBody(size):
	'''
		Make body of the packet from random bytes. returned as a string of bytes.
	'''
	return urandom(size)
	
def checkArguments(argv):
	try:
		opts, args = getopt(argv[1:],"hl:p:w:s:d:t:n:f:",["host", "portNumber", "PacketsPerWindows", "packetSize", 
						"duration", "time", "notificationPeriod","non-uniform"])
	except GetoptError:
		print 'UDPClient.py -l <hostname> -p <port> -s <packetSize> -w <PacketsPerWindows> -d <duration> -t <timeBetweenWindows>, -n <notificationPeriod>'
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
		elif opt in ('-s'):
			global packetSize
			packetSize = int(arg)
		elif opt in ('-w'):
			global PacketsPerWindows
			PacketsPerWindows = int(arg)
		elif opt in ('-d'):
			global duration
			duration = float(arg)
		elif opt in ('-t'):
			global timeBetweenWindows
			timeBetweenWindows = float(arg)
		elif opt in ('-n'):
			global notificationPeriod
			notificationPeriod = float(arg)
		elif opt in ('-f'):
			global nonUniform
			nonUniform = True

def getReceivedData(receivedDataQueue):
	'''
		Split the data and return an array. 
	'''
	# get received data
	recvData = receivedDataQueue.get()
	return recvData.split('time:', len(recvData))
			
def getSentData(packetsSendQueue, timeStampSendQueue): 
	'''
		Get sent data from the queue and return an array.
	'''
	arr = []
	arr.append(packetsSendQueue.get())
	arr.append(timeStampSendQueue.get())
	return arr

def calculateStatistics(recv, sent):
	'''
		This function will calculate the statisctics. 
		# ex loss rate: 24/25--> (1 -  24/25)*100
	'''
	return str(abs((1 - (int(recv) / int(sent)) * 100))) + "%"
	
def generateStatistics(queues):
	'''
		This function will make statistics.  
	'''
	
	fp  = open("log" + str(time()) + ".txt", 'a')
	
	while 1:
		recvArray = getReceivedData(queues[2])
		sentArray = getSentData(queues[0], queues[1])
		
		if int(sentArray[0]) != 0:
			lossRate = calculateStatistics(recvArray[0], sentArray[0])
		else: 
			lossRate = str(0) + "%"
	
		timeDifference = str(abs(float(recvArray[1]) - float(sentArray[1])))
		
		writeToLog(fp, lossRate + '\t' + timeDifference + '\t' + str(recvArray[0]) + '/' + str(sentArray[0]))		
		
def createConnection(): 
	'''
		make udp connection.
	'''
	print 'UDP target IP:', gethostbyname(host)
	print 'UDP target port:', port
	return socket(AF_INET, SOCK_DGRAM)

def setValues(args):
	'''
		set global values for the transmitter.
	'''
	global PacketsPerWindows, packetSize, duration, timeBetweenWindows 
	PacketsPerWindows = int(args[1])
	packetSize = int(args[0])
	duration = int(args[3])
	timeBetweenWindows = int(args[2])
	
def startSending(sock):
	'''
		This function will start sending packets.
	'''
	if nonUniform:
		# open input.txt
		p = open("input.txt", 'r')
		# get Generator for files 
		gen = readInput(p)
		# go over the values 
		for line in gen:
			#  parse the line and set values for the transmitter. 
			setValues(parseLine(line))
			# send packets
			total = sendUdpBasedOnDuration(sock)
		print 'finished reading file'
		p.close()
	else: 
		total = sendUdpBasedOnDuration(sock)
		
	return total
		
def launchThreads(startTime, queues):
	'''
		This function will launch all threads in the application.
	'''
	# statistics thread
	start_new_thread(generateStatistics, (queues,))
	
	# cancel pipe usage when called from cmd.
	if notificationPeriod != 0:
		# read from pipe
		start_new_thread(readFromPipe, (queues[2],))
	
		# put Values In Queue
		start_new_thread(putValuesInQueue, (startTime, queues[0], queues[1]))

def createQueues():
	'''
		packetsSendQueue 
		timeStampSendQueue  
		receivedDataQueue
	'''
	arr = [] 
	for x in range(3):
		arr.append(Queue())
	
	return arr
	
if __name__ == '__main__':
	
	checkArguments(argv)
	sock = createConnection()
	
	# queues 
	queues = createQueues()
	
	startTime = time()
	launchThreads(startTime, queues)
	
	totalNumberOfPacketsSend = startSending(sock)
	
	print "Number of packets sent:", totalNumberOfPacketsSend
	print 'closing sockets'
	
	sock.close()