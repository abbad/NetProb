'''
Created on Apr 13, 2013

@author: Abbad
'''
# Echo server program
import socket

HOST = "localhost"              # Symbolic name meaning all available interfaces
PORT = 4001                     # Arbitrary non-privileged port

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((HOST, PORT))

print "Server is listening.."

while 1:
    data  = sock.recv(1024)
    print "received message:\nsize:" + str(len(data))