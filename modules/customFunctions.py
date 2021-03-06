import logging
import os
def getTimestamp() :
    import time
    return time.strftime("%d/%m/%Y") + ' ' + time.strftime("%H:%M:%S")

def printToLog(stringToPrint, newline = 0) :
	#Print to console
	if newline:
		print '\n'
	print getTimestamp() + '\t' + stringToPrint
	#
	#Print to file
	logger = logging.getLogger("web2py.app.app")
	logger.setLevel(logging.DEBUG)
	logger.debug(stringToPrint)
	