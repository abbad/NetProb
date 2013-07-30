'''
Created on Apr 13, 2013

@author: Abbad
'''

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
# global variables 
host = "localhost"
port = 4001
windowSize = 10
packetSize = 1000
duration = 10
timeBetweenWindows = 0 
numberOfPackets = 1
notificationPeriod = 5 
# what the udp client send. 
packetsSendQueue = Queue()
# what the udp server has received. 
packetsRecievedQueue = Queue()
totalNumberOfPacketsSend = 0
threadFlag = False

# code to include subfolder modules (packages)
cmd_subfolder = osPath.realpath(osPath.abspath(osPath.join(osPath.split(getfile(currentframe()))[0],"subfolder")))
if cmd_subfolder not in path:
	path.insert(0, cmd_subfolder)

from utilities.udp_client_win32_named_pipes import *

def sendUdpBasedOntime(sock):
	'''
		sending packets based on duration
	'''
	startTime = time()
	stopDurationTime = startTime + duration
	notificationTime = startTime + notificationPeriod
	print 'UDP Client: sending packets for about ' + str(duration) + ' of seconds'
	global numberOfPackets, totalNumberOfPacketsSend
	numberOfPackets = 0
		
	while(1):
		# send a window a loop
		for i in range(windowSize):
		
			packet = makePacket(packetSize, numberOfPackets)
			sock.sendto(packet , (host, port))
			numberOfPackets = numberOfPackets + 1
			totalNumberOfPacketsSend = totalNumberOfPacketsSend + 1
			if notificationTime <= time():
				packetsSendQueue.put(numberOfPackets)
				numberOfPackets = 0
				notificationTime = time() + notificationPeriod
		
		if timeBetweenWindows != 0:
			print 'sleeping for ' + str(timeBetweenWindows) + ' seconds' 
			sleep(timeBetweenWindows)
		
		if stopDurationTime <= time():
			print 'done'
			break
			
def printHelp():
	print 'This is a UDP client:'
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
		opts, args = getopt(argv[1:],"hl:p:w:s:d:t:n:",["host", "portNumber", "windowSize", "packetSize", "duration", "Time", "notificationPeriod"])
	except GetoptError:
		print 'UDPClient.py -l <hostname> -p <port> -s <packetSize> -w <windowSize> -d <duration> -t <timeBetweenWindows>, -n <notificationPeriod>'
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
			global windowSize
			windowSize = int(arg)
		elif opt in ('-d'):
			global duration
			duration = float(arg)
		elif opt in ('-t'):
			global timeBetweenWindows
			timeBetweenWindows = float(arg)
		elif opt in ('-n'):
			global notificationPeriod
			notificationPeriod = float(arg)


def makeStatistics():
	'''
		This function to make statistics. It will compare what is received by udp server with what was send from udp client. 
	'''
	while 1:
		if threadFlag:
			break
		try: 
			print str(packetsRecievedQueue.get(timeout = 5)) + '/' + str(packetsSendQueue.get(timeout = 5))
		except Empty:
			pass
		
		
if __name__ == '__main__':
	
	checkArguments(argv)
	print 'UDP target IP:', gethostbyname(host)
	print 'UDP target port:', port
	sock = socket(AF_INET, SOCK_DGRAM)
	makeStatisticsThread = Thread(target = makeStatistics)
	makeStatisticsThread.start()
	start_new_thread(readFromPipe, ())
	sendUdpBasedOntime(sock)  
	threadFlag = True
	makeStatisticsThread.join()
	print "Number of packets sent:", totalNumberOfPacketsSend
	print 'closing sockets'
	
	sock.close()