'''
Created on June 23, 2013

@author: Abbad

Module to run the sender.

'''
from Tkinter import *
from subprocess import Popen

class Window(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent, background = "beige")
		self.parent = parent 
		self.interface()
	
	def interface(self):
		self.parent.title("Probing Delay Sender Application")
		self.pack(fill=BOTH, expand = 1) 
		self.setLabels()
		self.setButtons()
		self.setTextFields()
	
	'''
		This function will set buttons on the window.
	'''
	def setButtons(self):
		# exit button
		#exitbutton = Button(self, text = "Exit", foreground= "red", command = self.quit)
		#exitbutton.place(x= 150, y = 120)
		# start UDP Client button
		startUpdButton = Button(self, text = "Start UDP Client", foreground = "Black", command = launchUdpClient)
		startUpdButton.place(x = 30, y = 170)
		startTcpButton = Button(self, text = "Start TCP Server", foreground = "Black", command = launchTCPServer)
		startTcpButton.place(x = 340, y = 170) 
	
	'''
		This function will set the labels on the window.
	'''
	def setLabels(self):
		#UDP Client
		udp_hostLabel= Label(self, text = "Host Name", foreground = "Black")
		udp_hostLabel.place(x = 10, y = 10)
		
		udp_portLabel = Label(self, text = "Port Number", foreground = "Black")
		udp_portLabel.place(x = 10, y = 40)
		
		udp_packetSizeLabel = Label(self, text = "Packet Size", foreground = "Black")
		udp_packetSizeLabel.place(x = 10, y = 70)
		
		udp_packetScaleLabel = Label(self, text = "Byte", foreground = "Black")
		udp_packetScaleLabel.place(x = 220, y = 70)
		
		
		udp_timeBetweenEachWindowLabel = Label(self, text = "Time Between each Window", foreground = "Black")
		udp_timeBetweenEachWindowLabel.place(x = 10, y = 100) 
	
		udp_durationLabel = Label(self, text = "Duration Sending Packets", foreground = "Black")
		udp_durationLabel.place(x = 10, y = 130)
		
		# TCP Server
		tcp_portNumber = Label(self, text = "Port Number", foreground = "Black")
		tcp_portNumber.place(x = 340, y = 10)
	
	'''
		This function will set the text fields.
	'''	
	def setTextFields(self):
		#UDP Client
		# host 
		udp_hostEntry = Entry(self)
		udp_hostEntry.insert(0, "192.168.0.1")
		udp_hostEntry.place(x = 90, y = 10)
		# port
		udp_portEntry = Entry(self)
		udp_portEntry.insert(0, "5005")
		udp_portEntry.place(x = 90, y = 40)
		# packetSize
		udp_packetSizeEntry = Entry(self)
		udp_packetSizeEntry.insert(0, "1000")
		udp_packetSizeEntry.place(x = 90, y = 70)
		# Time Between Each Packet
		udp_timeBetweenEachPacket = Entry(self)
		udp_timeBetweenEachPacket.insert(0, "0")
		udp_timeBetweenEachPacket.place(x = 170, y = 100)
		# Duration
		udp_durationEntry = Entry(self)
		udp_durationEntry.insert(0, "10")
		udp_durationEntry.place(x = 170, y = 130)
		
		#TCP Server
		# Port
		tcp_portEntry = Entry(self)
		tcp_portEntry.insert(0, "5005")
		tcp_portEntry.place(x = 420, y = 10)

	'''
		This function will open the pipe to launch TCP server.
	'''
def launchTCPServer():
	print 'Starting TCP server'
	args = ["python", "TCP\TCPServer.py"]
	return(Popen(args, shell=False))
	
	'''
		This function will open a pipe and launch UDP Client.
	'''
def launchUdpClient():
	print 'Starting UDP client'
	args =  ["python", "UDP\UDPClient.py", "-d 400"]
	return(Popen(args, shell=False))		
		
def main():
	root = Tk()
	w = root.winfo_screenwidth()
	h = root.winfo_screenheight()
	root.geometry("%dx%d" % (w/2.3, h/3.6))
	app = Window(root)
	root = mainloop()
	
	
if __name__ == '__main__':
	main()
		
		