import serial
from time import sleep
from datetime import date
from datetime import datetime
from datetime import timedelta
from os import system
	
	

arduino = serial.Serial('/dev/ttyACM0', 9600)
d = date.today()
d_string = d.strftime("%y-%m-%d")
data_file = open(r"Data/"+d_string+".csv","w+")
print("Comms opened")
while True:
	t = datetime.now()
	var = arduino.readline()
	w = var.decode()[:-2]
	data_file.write(w+'\n')
	print(w)