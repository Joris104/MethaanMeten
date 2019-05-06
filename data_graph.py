import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


plt_min = 0
plt_max = 0.51
plt_sub = 0.05
time_max = 50	#TODO: detect this automagically
save_figure = True
datafile = "19-04-24.csv"
pins = [54]

if save_figure:
	filename = input("Please choose a name for the file\n")

print("Reading Data...")
data = pd.read_csv("Data/"+datafile, encoding="utf-8",index_col=0)

l = len(data.loc[pins[0]].values[:,1])
voltage_data = np.zeros((len(pins),l))

time_data = np.zeros((len(pins),l))
for i in range(0,len(pins)):
	voltage_data[i] = data.loc[pins[i]].values[:,1]
	time_data[i] = data.loc[pins[i]].values[:,0]/(1000*60*60)

voltage_data *= 5 / 1023 
#Handle the colors
tableau = [(31,119,180),(174,199,180),(255,124,14)]
for i in range(len(tableau)):
	r,g,b = tableau[i]
	tableau[i] = (r/255.,g/255.,b/255.)

print("Plotting Data...")
#Create a figure
plt.figure(figsize = (12,9))
ax = plt.subplot(111)    
ax.spines["top"].set_visible(False)    
ax.spines["bottom"].set_visible(False)    
ax.spines["right"].set_visible(False)    
ax.spines["left"].set_visible(False) 

plt.ylim(plt_min,plt_max)

plt.yticks(np.arange(plt_min,plt_max,plt_sub), fontsize=14)   


for y in np.arange(plt_min,plt_max,plt_sub):    
    plt.plot(range(0,round(time_max)), [y]*round(time_max), "--", lw=0.5, color="black", alpha=0.3)  
	
for i in range(len(pins)):
	plt.plot(time_data[i],voltage_data[i])

plt.title("Voltage across the methane sensing resistor, in function of time (in hours)", fontsize=17, ha="center") 

if save_figure :
	plt.savefig(filename+".png")
else : 
	plt.show()