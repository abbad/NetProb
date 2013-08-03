'''
Created on July 23, 2013

@author: Abbad

Module to run non-uniform probing.

'''

from Tkinter import Frame, Tk, BOTH, Label, Button, Entry, mainloop
from subprocess import Popen
from os import pipe, fdopen, read
from os import path as osPath
from inspect import currentframe, getfile
from sys import path
from thread import start_new_thread
from utilities.user_pipes import getHandleDuplicate, closePipe	
from utilities.file_io import *
from Tkinter import *
	
class Window(Frame):
			
	def __init__(self, parent):
		Frame.__init__(self, parent, background = "beige")
		self.parent = parent 
		self.interface()
	
	def interface(self):
		self.parent.title("Probing Delay Transmitter Application")
		self.pack(fill=BOTH, expand = 1) 
		self.setLabels()
		self.setButtons()
		self.setTextFields()
	
	
	def setButtons(self):
		'''
			This function will set buttons on the window.
		'''
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
		global startThreadFlag
		startThreadFlag = True
		self.startButton.config(state = NORMAL)
		terminateProcesses()
	
	def callStartByThread(self):
		'''
			This function will call start function by a thread. 
		'''
		self.startButton.config(state = DISABLED)
		start_new_thread(self.start, ())
		
	
	def setLabels(self):
		'''
			This function will set the labels on the window.
		'''
		#UDP Client
		udp_label = Label(self, text = "UDP Client", foreground = "Black")
		udp_label.place(x = 40, y = 10)
		
		udp_hostLabel= Label(self, text = "Host Name", foreground = "Black")
		udp_hostLabel.place(x = 10, y = 40)
		
		udp_portLabel = Label(self, text = "Port Number", foreground = "Black")
		udp_portLabel.place(x = 10, y = 70)
		
		# TCP Server		
		tcp_label = Label(self, text = "TCP Server", foreground = "Black")
		tcp_label.place(x = 360, y = 10)
		
		tcp_hostEntry = Label(self, text = "Host Name", foreground = "Black")
		tcp_hostEntry.place( x= 340, y = 40)
		
		tcp_portNumber = Label(self, text = "Port Number", foreground = "Black")
		tcp_portNumber.place(x = 340, y = 70)
		
		#global 
		notification_period = Label(self, text = "Notification Period", foreground = "Black")
		notification_period.place(x = 310, y = 100)
	
	
	def setTextFields(self):
		'''
			This function will set the text fields.
		'''	
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

		# Notification period
		self.notificationEntry = Entry(self)
		self.notificationEntry.insert(0, "5")
		self.notificationEntry.place(x = 420, y = 100)
	
	def launchTCPServer(self, pipeArg):
		'''
			This function will open a sub-process to launch TCP server.
		'''
		global P1
		print 'Starting TCP server'
		args = ["python", "TCPServer.py", "-l", str(self.tcp_hostEntry.get()) ,"-p", str(self.tcp_portEntry.get()), "-n", str(self.notificationEntry.get()), "-a", pipeArg]
		P1 = Popen(args, shell=False)
		
	def launchUdpClient(self, para):
		'''
			This function will open a sub-process and launch UDP Client.
		'''
		global P2
		print 'Starting UDP Server'
		args =  ["python", "UDPServer.py", "-l", str(self.udp_hostEntry.get()), "-p", str(self.udp_portEntry.get()), "-s", para[0], "-t"
				, para[2], "-w", para[1], "-n", str(self.notificationEntry.get()), "-d", para[3]]
		P2 = Popen(args, shell=False)		
	
	def launchUdpClientNonUniform(self):
		'''
			This function will read from the input.txt and launch udp client with the specific values. 
		'''
		# open input.txt
		p = openFile("input.txt")
		# get Generator for files 
		gen = readInput(p)
		# go over the values 
		for line in gen:
			# parse the line 
			input = parseLine(line)
			# launch udp client with the values
			self.launchUdpClient(input)
			P2.wait()
			if startThreadFlag:
				break
		
		print 'finished reading file'
			
	def start(self):
		'''
			This function will start 1. Tcp Server, 2. Udp Client.
		'''
		global startThreadFlag 
		startThreadFlag = False
		# Create pipe for communication
		pipeOut, pipeIn = pipe()
		
		pipeInDup = getHandleDuplicate(pipeIn)
		
		self.launchTCPServer(str(int(pipeInDup)))
		
		# Close write end of pipe in parent
		closePipe(pipeIn, pipeInDup)
		
		pipefh = fdopen(pipeOut, 'r')
		message = pipefh.read()
		# a message to start udp server
		if(message == "startUdpClient"):
			self.launchUdpClientNonUniform()
				 
	
		pipefh.close()
		
		
# global variables 

ROOT = None 
P1 = None
P2 = None
startThreadFlag = False

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
	
def terminateProcesses():
	''' this will terminate the processes running '''
	global P1, P2
	try: 
		if P1:
			P1.terminate()
	except:
		pass
	try:
		if P2:
			P2.terminate()
	except: 
		pass

	
if __name__ == '__main__':
	# testing
	#f = openFile()
	#gen = readInput(f)
	#for c in gen:
	#	print parseInput(c)
	main()
