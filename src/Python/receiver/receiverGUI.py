'''
Created on July 23, 2013

@author: Abbad

Module to run the receiver(tcp client and udp server).

'''


from Tkinter import Frame, Tk, BOTH, Label, Button, Entry, mainloop
from subprocess import Popen
from os import pipe, fdopen, read
from os import path as osPath
from inspect import currentframe, getfile
from sys import path
from thread import start_new_thread
from utilities.user_pipes import getHandleDuplicate, closePipe	
from Tkinter import *


class Window(Frame):
			
	def __init__(self, parent):
		Frame.__init__(self, parent, background = "beige")
		self.parent = parent 
		self.interface()
	
	def interface(self):
		self.parent.title("Probing Delay Receiver Application")
		self.pack(fill=BOTH, expand = 1) 
		self.setLabels()
		self.setButtons()
		self.setTextFields()
	
	'''
		This function will set buttons on the window.
	'''
	def setButtons(self):
		# exit button
		# exitbutton = Button(self, text = "Exit", foreground= "red", command = self.quit)
		# exitbutton.place(x= 150, y = 120)
		# start UDP Client button
		# only one start button
		self.startButton = Button(self, text = "Start", foreground = "Black", command = self.callStartByThread)
		self.startButton.place(x = 30, y = 220)
		# stop button
		stopButton = Button(self, text = "Stop", foreground = "Black", command = self.callTerminateProcesses)
		stopButton.place(x = 90, y = 220)
		
		#startTcpButton = Button(self, text = "Start TCP Server", foreground = "Black", command = self.launchTCPServer)
		#startTcpButton.place(x = 340, y = 190) 
	
	def callTerminateProcesses(self):
		'''
			This function will change the state of the start button and also stop the processes. 
		'''
		self.startButton.config(state = NORMAL)
		terminateProcesses()
	
	def callStartByThread(self):
		'''
			This function will call start function by a thread. 
		'''
		self.startButton.config(state = DISABLED)
		start_new_thread(self.start, ())
		
	'''
		This function will set the labels on the window.
	'''
	def setLabels(self):
		#UDP Server
		udp_label = Label(self, text = "UDP Server", foreground = "Black")
		udp_label.place(x = 40, y = 10)
		
		udp_hostLabel= Label(self, text = "Host Name", foreground = "Black")
		udp_hostLabel.place(x = 10, y = 40)
		
		udp_portLabel = Label(self, text = "Port Number", foreground = "Black")
		udp_portLabel.place(x = 10, y = 70)
		
		
		# TCP Client		
		tcp_label = Label(self, text = "TCP Client", foreground = "Black")
		tcp_label.place(x = 360, y = 10)
		
		tcp_hostEntry = Label(self, text = "Host Name", foreground = "Black")
		tcp_hostEntry.place( x= 340, y = 40)
		
		tcp_portNumber = Label(self, text = "Port Number", foreground = "Black")
		tcp_portNumber.place(x = 340, y = 70)
		
	'''
		This function will set the text fields.
	'''	
	def setTextFields(self):
		#UDP Client
		# host 
		self.udp_hostEntry = Entry(self)
		self.udp_hostEntry.insert(0, "127.0.0.1")
		self.udp_hostEntry.place(x = 90, y = 40)
		# port
		self.udp_portEntry = Entry(self)
		self.udp_portEntry.insert(0, "4001")
		self.udp_portEntry.place(x = 90, y = 70)
		
		#TCP Server
		# Host Name
		self.tcp_hostEntry = Entry(self)
		self.tcp_hostEntry.insert(0, "127.0.0.1")
		self.tcp_hostEntry.place(x = 420, y = 40)
		
		# Port
		self.tcp_portEntry = Entry(self)
		self.tcp_portEntry.insert(0, "5005")
		self.tcp_portEntry.place(x = 420, y = 70)

	'''
		This function will open a sub-process to launch TCP client.
	'''
	def launchTcpClient(self, pipeArg):
		global P1
		print 'Starting TCP client'
		args = ["python", "TCPClient.py", "-l", str(self.tcp_hostEntry.get()) ,"-p", str(self.tcp_portEntry.get()), "-a", pipeArg]
		P1 = Popen(args, shell=False)
		
	'''
		This function will open a sub-process and launch UDP server.
	'''
	def launchUdpServer(self, notificationPeriod):
		global P2
		print 'Starting UDP Server'
		args =  ["python", "UDPServer.py", "-l", str(self.udp_hostEntry.get()), "-p", str(self.udp_portEntry.get()),  "-n", notificationPeriod]
		P2 = Popen(args, shell=False)		

	'''
		This function will start 1. Tcp Server, 2. Udp Client.
	'''
	def start(self):
		# Create pipe for handshake
		handShake = CreatePipeBetweenParentAndTcpClient()
		
		# Start child with argument indicating which FD/FH to read from
		TCPsubproc = self.launchTcpClient(str(int(handShake[2])))
						
		# Close write end of the pipe in parent
		closePipe(handShake[1], handShake[2])
		
		# wait for message from tcp client
		message = getMessageFromTcpClient(handShake[0])
	
		if(message[0:14] == "startUdpServer"):
			UDPServerSubProc = self.launchUdpServer(message[14:])

'''
	create a pipe between parent and tcp client. 
'''
def CreatePipeBetweenParentAndTcpClient():
	pipeout, pipein = pipe()
	
	pipeInDuplicate = getHandleDuplicate(pipein)
	
	return pipeout, pipein, pipeInDuplicate

'''
	get message from tcp client, which it got from the sender part of the program.
'''
def getMessageFromTcpClient(pipeout):
	pipefh = fdopen(pipeout, 'r')
	message = pipefh.read()
	pipefh.close()
	return message	
		
# global variables 

ROOT = None 
P1 = None
P2 = None

def main():
	global ROOT 
	ROOT = Tk()
	ROOT.protocol('WM_DELETE_WINDOW', terminateAll)
	w = ROOT.winfo_screenwidth()
	h = ROOT.winfo_screenheight()
	ROOT.geometry("%dx%d" % (w/1.6, h/3))
	app = Window(ROOT)
	ROOT = mainloop()


def terminateAll():
	global ROOT 
	terminateProcesses() 
	ROOT.destroy()
	
''' this will terminate the processes running '''

def terminateProcesses():
	global P1, P2
	try: 
		if P1:
			P1.terminate()
	except:
		print "error terminating p1"
	try:
		if P2:
			P2.terminate()
	except: 
		print "error terminating p2"
	
	
if __name__ == '__main__':
	main()
	