'''
Created on May 7, 2013

@author: Abbad
'''

'''
	this is for interpreting the packet
'''

def getPacketSequenceNumber(packet):
	'''
		first 32 bytes are the sequence number
	'''
	return int(data[0:32], 2)

	