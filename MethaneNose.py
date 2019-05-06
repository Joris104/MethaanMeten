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
#########    Variables to set in script    							 ########
####################################################

#Port has to be set to the USB port connected to the Arduino. Format :  '/dev/{something}' on Linux, 'COM{something}' on Windows
#filename is the name of the file where data is saved. 'None' simply uses the date of the measurement. Extention is added automatically and should not be added here0
#debug controls how much info is displayed on the command prompt. Levels are 0,1 and 2
#pins controls which pins we are collecting data from
#dataDiscard controls how many data points are discarded at the start of an experiment before the data is considered trustworthy
port = '/dev/ttyACM0'
filename = None 
debug = 1 
pins = [54] 
dataDiscard = 5

####################################################
#########         Variable Handling        								  ########
####################################################

#We set the filename to the date if none was specified

exitFlag = False #Setting this flag to true will close the connection with the Arduino
if filename == None:
		d = date.today()
		filename = d.strftime("%y-%m-%d")
	
	
####################################################
#########         Live Plot Handler         								########
####################################################
 
#This draws the live plot 

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
			#Sometimes, faultive data gets through (for example a line with too many arguments). This simply ignores such a line and continues on the next one
		try:
			idx = pins.index(int(pin))
		except:
			if debug >0:
				print("Tried to plot data from pin",pin,"but this pin was not declared")
				return
		
		ys[idx].append(float(measurement))
		xs[idx].append(int(time)/1000)
		
	
	ax1.clear()
	for i in range(len(pins)):
		ax1.plot(xs[i],ys[i])
		if debug > 1:
			print('Data plotted')
	
style.use('fivethirtyeight')
fig = plt.figure()
ax1	= fig.add_subplot(1,1,1)

def animationHandler(fig):
	global exitFlag
	ani = animation.FuncAnimation(fig,animate,fargs=(port,filename,debug,pins), interval = 1000)
	plt.show()
	#This part of the code only executes once the plot was closed by the user
	exitFlag = True 

#####################################################
#########        Connection Handler         							   #########
#####################################################

def arduinoHandler(port,filename,debug,pins):
	#This handles the connection with the Arduino
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
	#The first data is discarded to avoid previous experiments  contaminating this one
	dataNum = 0
	while True:
		try:
			var = arduino.readline()
			if dataNum < dataDiscard :
				dataNum +=1
				continue
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
			#Sometimes the Arduino sends incomplete data. This handles such a case
			if debug > 1:
				print("A ValueError occured. The data recieved from the arduino :"+w)
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
##########                     Threading                  													#########
###################################################################


arduinoThread = threading.Thread(target=arduinoHandler, args=(port,filename,debug,pins))
arduinoThread.start()
animationHandler(fig)
