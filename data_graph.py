import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv(r"C:\Users\utilisateur\Documents\_Ugent\VOP\Arduino code\Python\19-03-11.csv",encoding="utf-8",index_col=0)
index = [54,58,62]
voltage_data = np.zeros((3,356))
for i in range(0,3):
	voltage_data[i] = data.loc[index[i]].values[:356,0]
	
voltage_data *= 5/1023
#Handle the colors
tableau = [(31,119,180),(174,199,180),(255,124,14)]
for i in range(len(tableau)):
	r,g,b = tableau[i]
	tableau[i] = (r/255.,g/255.,b/255.)

#Create a figure
plt.figure(figsize = (12,9))
ax = plt.subplot(111)    
ax.spines["top"].set_visible(False)    
ax.spines["bottom"].set_visible(False)    
ax.spines["right"].set_visible(False)    
ax.spines["left"].set_visible(False) 

plt.ylim(0, 2.5)

plt.yticks(np.arange(0,2.501,0.5), fontsize=14)    
plt.xticks(np.arange(0,len(voltage_data[0])*15,15*60),[str(x/60) for x in range(0,len(voltage_data[0])*15,15*60)], fontsize=14) 

for y in np.arange(0,2.51,0.5	):    
    plt.plot(range(0,len(voltage_data[0])*15,15), [y] * len(voltage_data[0]), "--", lw=0.5, color="black", alpha=0.3)  
	
for i in range(3):
	plt.plot(np.arange(0,len(voltage_data[0])*15,15),voltage_data[i])

plt.title("Voltage across the methane sensing resistor, in function of time (in minutes)", fontsize=17, ha="center")  


plt.savefig("voltage_methane_sensor_all.png")