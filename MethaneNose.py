import serial
import threading
from time import sleep
from datetime import date
from datetime import datetime
from datetime import timedelta
from os import system
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
####################################################
#########    Variables to set in script     ########
####################################################

port = 'COM3'	#format : '/dev/{something}' on Linux, 'COM{X}' on Windows
filename = None #set to none to just use the date. Extension is added automatically
debug = 1 #set to 1 for more debug info
pins = [14] #the pins we will be collecting data on

####################################################
#########         Variable Handling         ########
####################################################
exitFlag = False
if filename == None:
		d = date.today()
		filename = d.strftime("%y-%m-%d")
	
	
####################################################
#########         Live Plot Handler         ########
####################################################

def animate(i, port, filename, debug, pins):
	if filename == None:
			return
	try:
		graph_data = open("Data/"+filename+'.csv','r').read()
		if debug > 1:
			print("Successfully opened file", flush = True)
	except IOError:
		if debug > 0:
			print("WARNING : Tried to open 'Data/"+filename+".csv' but failed.",sep='')
		return
	lines = graph_data.split('\n')
	ys=[[] for i in range(len(pins))]
	xs=[[] for i in range(len(pins))]
	for line in lines:
		try:
			pin,time,measurement = line.split(',')
		except:
			continue
		try:
			idx = pins.index(int(pin))
		except:
			if debug >0:
				print("Tried to plot data from pin",pin,"but this pin was not declared")
				return
		
		ys[idx].append(int(measurement))
		xs[idx].append(int(time)/1000)
		
	
	ax1.clear()
	for i in range(len(pins)):
		ax1.plot(xs[i],ys[i])
		if debug > 1:
			print('Data plotted success')
	
style.use('fivethirtyeight')
fig = plt.figure()
ax1	= fig.add_subplot(1,1,1)

def animationHandler(fig):
	global exitFlag
	ani = animation.FuncAnimation(fig,animate,fargs=(port,filename,debug,pins), interval = 1000)
	plt.show()
	exitFlag = True

#####################################################
#########        Connection Handler         #########
#####################################################

def arduinoHandler(port,filename,debug,pins):
	#Arduino Handler
	global exitFlag
	try :
		arduino = serial.Serial(port, 9600)
		print("Serial Communication with the Arduino : OK")
	except :
		print("ERROR : unable to locate Arduino at port",port)
		sys.exit()
	#File Handler
	
	try:
		data_file = open(r"Data/"+filename+".csv","w+")
	except:
		print("ERROR : unable to open Data/",filename,sep='')
		sys.exit()
	else:
		print("Data will be saved to Data/",filename,sep='')

	#Communicating with the Arduino and saving the data	
	while True:
		try:
			var = arduino.readline()
			w = var.decode()[:-2] #This is to cut the '\n' - useful if we are printing to the cmd shell
			pin, time, measurement = w.split(',')
			data_file.write(w+'\n')
			data_file.flush()
			if debug > 0:
				print("pin : ",pin," || time (s): ",str(int(time)/1000)," || ",measurement,sep='',flush=True)
			
			if exitFlag:
				data_file.close()
				arduino.close()
				print("Closing Arduino Connection...", flush=True)
				sleep(3)
				break
		# Handling a KeyboardInterrupt
		except (KeyboardInterrupt):
			data_file.close()
			arduino.close()
			print("Keyboard Interruption - closing")
			break
		except ValueError:
			continue
		#Handling unexpected errors
		except:
			print("ERROR : an unexpected error happened")
			try:
				data_file.close()
				arduino.close()
			except:
				print("Could NOT close the data file and/or Arduino connection properly - data may have been lost or corrupted")
				print("It is recommended to unplug the Arduino before launching this script again to avoid further errors")
			finally:
				raise
###################################################################
##########                     Threading                  #########
###################################################################


arduinoThread = threading.Thread(target=arduinoHandler, args=(port,filename,debug,pins))
arduinoThread.start()
#arduinoHandler(port,filename,debug,pins)
animationHandler(fig)
