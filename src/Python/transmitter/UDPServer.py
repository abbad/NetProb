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
from sys import path
from Queue import Queue, Empty
from threading import Thread 
from utilities.file_io import writeToLog, readInput, parseLine
from utilities.udp_server_win32_named_pipes import *

# global variables 
host = "localhost"
port = 4001
packetsPerWindows = 10
packetSize = 1000
duration = 10
timeBetweenWindows = 0 
numberOfPackets = 1
notificationPeriod = 0
totalNumberOfPacketsReceived = 0
logFileName = "log" + str(time()) + ".log"
timeBetweenPacket = 0
# flags
nonUniform = False
# remainder of the recieved packets, to be added to the next lost packets
recievedPacketsRemainder = 0

def printHelp():
	print 'This is a UDP Server:'
	print 'usage:'
	print '-l Host \t\t\t default localhost'
	print '-p port number \t\t\t default 4001'
	print '-s packet size \t\t\t default 50'
	print '-t time between each window \t default 0 seconds'
	print '-w window size \t\t\t default 0'
	print '-d duration sending packets \t dafault 20'
	print '-n notification period \t default 0 \n'
	print '-x time between each packet \t default 0\n'

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
		for i in range(packetsPerWindows):	
			packet = makePacket(packetSize, numberOfPackets)
			sock.sendto(packet , (host, port))
			numberOfPackets = numberOfPackets + 1
			totalNumberOfPacketsSend = totalNumberOfPacketsSend + 1
			
			# timeBetweenPacket
			sleep(timeBetweenPacket)
			
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
		opts, args = getopt(argv[1:],"hl:p:w:s:d:t:n:f:x:",["host", "portNumber", "packetsPerWindows", "packetSize", 
						"duration", "time", "notificationPeriod","non-uniform", "timeBetweenPacket"])
	except GetoptError:
		print 'UDPClient.py -l <hostname> -p <port> -s <packetSize> -w <packetsPerWindows> -d <duration> -t <timeBetweenWindows> -x <timeBetweenPacket>'
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
			global packetsPerWindows
			packetsPerWindows = int(arg)
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
		elif opt in ('-x'):
			global timeBetweenPacket
			timeBetweenPacket = float(arg)

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

def calculateRatio(recv, sent):
	'''
		This function will calculate ratio . 
		# ex loss rate: 24/25--> (1 -  24/25)*100
	'''
	global recievedPacketsRemainder
	recv = int(recv)
	# check if recv greater then sent 
	if recv > sent:
		print 'recv > sent'
		# subtract a sum from the recieved so its equal to the send packets.
		recievedPacketsRemainder = recv - sent
		return sent ,"0%"
		
	
	# re add the remainder of the recieved to the actual recieved packets. 
	recv = recv + recievedPacketsRemainder
	recievedPacketsRemainder = 0
	return int(recv), str(abs(((1 - float(recv) / float(sent)) * 100))) + "%"
	
def generateStatistics(queues, ):
	'''
		This function will make statistics.  
	'''
	global totalNumberOfPacketsReceived
	
	while 1:
		fp  = open(logFileName, 'a')
		recvArray = getReceivedData(queues[2])
		sentArray = getSentData(queues[0], queues[1])
		totalNumberOfPacketsReceived += int(recvArray[0]) 
		if int(sentArray[0]) != 0:
			recv, lossRate = calculateRatio(recvArray[0], sentArray[0])
		else: 
			lossRate = str(0) + "%"
	
		timeDifference = str(float(recvArray[1]) - float(sentArray[1]))
		
		writeToLog(fp, lossRate + '\t' + timeDifference + '\t' + str(recv) + '/' + str(sentArray[0]))	
		
		fp.close()
		
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
	global packetsPerWindows, packetSize, duration, timeBetweenWindows 
	packetSize = int(args[0])
	packetsPerWindows = int(args[1])
	timeBetweenPacket = float(args[2])
	timeBetweenWindows = float(args[3])
	duration = int(args[4])
	
def startSending(sock):
	'''
		This function will start sending packets.
	'''
	total = 0
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
			total += sendUdpBasedOnDuration(sock)
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
	
	# if statement to cancel pipe usage when called from cmd.
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
	totalNumberOfPacketsSend = 0
	checkArguments(argv)
	sock = createConnection()
	
	# queues 
	queues = createQueues()
	launchThreads(time(), queues)
	
	totalNumberOfPacketsSend = startSending(sock)
	fp  = open(logFileName, 'a')
	sleep(2)
	
	print totalNumberOfPacketsReceived, totalNumberOfPacketsSend
	writeToLog(fp, calculateRatio(totalNumberOfPacketsReceived, totalNumberOfPacketsSend)[1])
	print "the average packet loss ratio of all the calculated packet losses", calculateRatio(totalNumberOfPacketsReceived, totalNumberOfPacketsSend)[1]
	fp.close()
	print 'closing sockets'
	
	sock.close()
