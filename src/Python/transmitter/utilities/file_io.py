'''
	Helping module for file handling and parsing strings. 
'''

from re import compile
	
def readInput(file):
	'''
		This function will read from input file. It will return a generator.
	'''	
	# reading from the 4th line 
	for i, line in enumerate(file):
		if i > 2:
			yield line

def parseLine(line):
	'''
		This function will parse the line sent to by commas
	'''
	p = compile('[,;\s]+')
	return p.split(line)

def writeToLog(filePointer, value):
	'''
		This function will write the output of the application into the log file. 
	'''
	filePointer.write(value + '\n')