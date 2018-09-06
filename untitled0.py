# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 15:19:58 2018

@author: pnola
"""

#from mpl_toolkits.basemap import Basemap
import functions as f
from scipy.interpolate import griddata
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')
ross4= [-106.040772,37.780315]
schmale4 = [-106.0422978,37.78155488]
ground = [-106.03917,37.781644]
<<<<<<< HEAD

plt.scatter(ross4[0],ross4[1])
plt.scatter(schmale4[0],schmale4[1])
plt.scatter(ground[0],ground[1])
"""
=======
>>>>>>> 59c3ef21aa68d607891b05e14f6ba28cb98bbfba
print(f.lonlat2m(schmale4[0],schmale4[1],ross4[0],ross4[1]))

ross4 = f.lonlat2m(ground[0],ground[1],ross4[0],ross4[1])
schmale4 = f.lonlat2m(ground[0],ground[1],schmale4[0],schmale4[1])
print(ross4)
print(schmale4)
ground = [0,0]
dx=ross4[0]-schmale4[0]
dy=schmale4[1]-ross4[1]
print('dx = '+str(dx),'dy = '+str(dy))


ross4_data = pd.read_csv('Ross4_DroneMetData.txt', delim_whitespace=True,header=1,names=['date','time','wind_speed','wind_dir','temp'])
seconds = []
for t in range(ross4_data.shape[0]):
    hrs_in_sec = int(ross4_data['time'][t][0:2])*3600
    min_in_sec = int(ross4_data['time'][t][3:5])*60
    sec = int(ross4_data['time'][t][6:8])
    seconds.append(hrs_in_sec+min_in_sec+sec)
ross4_data['time'] = seconds

schmale4_data = pd.read_csv('Schmale4_DroneMetData.txt', delim_whitespace=True,header=1,names=['date','time','wind_speed','wind_dir','temp'])
seconds = []
for t in range(schmale4_data.shape[0]):
    hrs_in_sec = int(schmale4_data['time'][t][0:2])*3600
    min_in_sec = int(schmale4_data['time'][t][3:5])*60
    sec = int(schmale4_data['time'][t][6:8])
    seconds.append(hrs_in_sec+min_in_sec+sec)
schmale4_data['time'] = seconds

ground_data = pd.read_csv('Ground2_MetData.txt', delim_whitespace=True,header=1,names=['date','time','wind_speed','wind_dir','temp'])
seconds = []
for t in range(ground_data.shape[0]):
    hrs_in_sec = int(ground_data['time'][t][0:2])*3600
    min_in_sec = int(ground_data['time'][t][3:5])*60
    sec = int(ground_data['time'][t][6:8])
    seconds.append(hrs_in_sec+min_in_sec+sec)
ground_data['time'] = seconds

min_time = max([ross4_data['time'].min(),schmale4_data['time'].min(),ground_data['time'].min()])
max_time = min([ross4_data['time'].max(),schmale4_data['time'].max(),ground_data['time'].max()])
#print([x for x in ground_data['time'] if min_time < x and x < max_time])
ross4_data=ross4_data[min_time<=ross4_data['time']]
ross4_data=ross4_data[ross4_data['time']<=max_time]

schmale4_data=schmale4_data[min_time<=schmale4_data['time']]
schmale4_data=schmale4_data[schmale4_data['time']<=max_time]

ground_data=ground_data[min_time<=ground_data['time']]
ground_data=ground_data[ground_data['time']<=max_time]
s1=[]
points = [(ross4[0],ross4[1]),(schmale4[0],schmale4[1]),(ground[0],ground[1])]
for t in range(ground_data.shape[0]):
    if ground_data.iloc[t]['time'] != schmale4_data.iloc[t]['time'] or ground_data.iloc[t]['time'] != ross4_data.iloc[t]['time']:
        print('ERROR: Sample Time Inequal @ {0}'.format(t))
        break
    values = [ross4_data.iloc[t]['wind_speed'],schmale4_data.iloc[t]['wind_speed'],ground_data.iloc[t]['wind_speed']]
    wind_speed = griddata(points,values,(ross4[0],schmale4[1]),method='cubic')
    values = [ross4_data.iloc[t]['wind_dir'],schmale4_data.iloc[t]['wind_dir'],ground_data.iloc[t]['wind_dir']]
    wind_dir = griddata(points,values,(ross4[0],schmale4[1]),method='cubic')
    u = wind_speed*np.cos(wind_dir)
    v = wind_speed*np.sin(wind_dir)
    #u_ground = ground_data.iloc[t]['wind_speed']*np.cos(ground_data.iloc[t]['wind_dir'])
    #v_ground = ground_data.iloc[t]['wind_speed']*np.sin(ground_data.iloc[t]['wind_dir'])
    u_schmale = schmale4_data.iloc[t]['wind_speed']*np.cos(schmale4_data.iloc[t]['wind_dir'])
    v_schmale = schmale4_data.iloc[t]['wind_speed']*np.sin(schmale4_data.iloc[t]['wind_dir'])
    u_ross = ross4_data.iloc[t]['wind_speed']*np.cos(ross4_data.iloc[t]['wind_dir'])
    v_ross = ross4_data.iloc[t]['wind_speed']*np.sin(ross4_data.iloc[t]['wind_dir'])
    '''
    dudx = (u_schmale-u)/dx
    dudy = (u-u_ross)/dy
    dvdx = (v_schmale-v)/dx
    dvdy = (v-v_ross)/dy
    '''
    dudx = (u-u_schmale)/dx
    dudy = (u_ross-u)/dy
    dvdx = (v-v_schmale)/dx
    dvdy = (v_ross-v)/dy
    
    J = np.array([[dudx,dudy],[dvdx,dvdy]])
    S = 0.5*(J+J.T)
    s1.append(np.linalg.eig(S)[0].min())
    
hrs, sec = np.divmod(ross4_data['time'],3600)
#mins, sec = np.divmod(mins,60)

#plot_time = []
#for t in range(ground_data.shape[0]):
#    plot_time.append(str(hrs[t])+':'+str(mins[t])+':'+str(sec[t]))

plt.plot(sec,s1)
plt.title('s$_{1}$ from ross4 & schmale4 flight')
plt.xlabel('seconds since 1600hrs Mountain Time, 2018-07-14')
plt.ylabel('sec$^{-1}$')
plt.savefig('s1_colorado_campaign.png', transparent=False, bbox_inches='tight',pad_inches=0)




#"""