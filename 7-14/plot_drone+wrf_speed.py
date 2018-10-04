# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 15:19:58 2018

@author: pnola
"""

#from mpl_toolkits.basemap import Basemap
import functions as f
from scipy.interpolate import griddata, RegularGridInterpolator
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time as t_func
plt.close('all')

F = np.load('wrf_les_speed.npz')
x = F['x']
y = F['y']
wrf_time = F['time']
t0 = t_func.gmtime(wrf_time[0]).tm_hour-6
tf = t_func.gmtime(wrf_time[-1]).tm_hour-6
wrf_time = np.linspace(t0,tf,wrf_time.shape[0])
proj_center_lon = F['proj_center_lon']
proj_center_lat = F['proj_center_lat']
speed_wrf = F['speed']
F.close()
ground5 = [-106.041504,37.782005]
ground = ground5

ross_lon = np.mean([-106.04076,-106.040763,-106.040762,-106.040762])
ross_lat = np.mean([37.780287,37.780307,37.780398,37.780338])

schmale_lon = np.mean([-106.0422848,-106.0422905,-106.0422956,-106.0422941])
schmale_lat = np.mean([37.78153018,37.78155617,37.78156052,37.78156436])
#(ross, schmale)
paired_flights = [(22,9),(23,10),(25,11),(26,12)]

ground_m = f.lonlat2m(proj_center_lon,proj_center_lat,ground[0],ground[1])
ross_pos_m = f.lonlat2m(proj_center_lon,proj_center_lat,ross_lon,ross_lat)
schmale_pos_m = f.lonlat2m(proj_center_lon,proj_center_lat,schmale_lon,schmale_lat)
dx = ground_m[0] - schmale_pos_m[0]
dy = ground_m[1] - schmale_pos_m[1]
points = (wrf_time,y,x)
[yi,zi,xi] = np.meshgrid(schmale_pos_m[1],wrf_time,ground_m[0])
Xi = (zi.ravel(),yi.ravel(),xi.ravel())
fspeed = RegularGridInterpolator(points,speed_wrf)
speed_plot = fspeed(Xi)

speed=[]
plt_sec=[]
for i, pair in enumerate(paired_flights):
    plt_sec_temp = []
    speed_temp = []
    
    ross_data = pd.read_csv('Ross{:d}_DroneMetData.txt'.format(pair[0]), delim_whitespace=True,header=1,names=['date','time','wind_speed','wind_dir','temp'])
    seconds = []
    for t in range(ross_data.shape[0]):
        hrs_in_sec = int(ross_data['time'][t][0:2])*3600
        min_in_sec = int(ross_data['time'][t][3:5])*60
        sec = int(ross_data['time'][t][6:8])
        seconds.append(hrs_in_sec+min_in_sec+sec)
    ross_data['time'] = seconds
    
    schmale_data = pd.read_csv('Schmale{:d}_DroneMetData.txt'.format(pair[1]), delim_whitespace=True,header=1,names=['date','time','wind_speed','wind_dir','temp'])
    seconds = []
    for t in range(schmale_data.shape[0]):
        hrs_in_sec = int(schmale_data['time'][t][0:2])*3600
        min_in_sec = int(schmale_data['time'][t][3:5])*60
        sec = int(schmale_data['time'][t][6:8])
        seconds.append(hrs_in_sec+min_in_sec+sec)
    schmale_data['time'] = seconds

    ground_data = pd.read_csv('Ground5_MetData.txt', delim_whitespace=True,header=1,names=['date','time','wind_speed','wind_dir','temp'])
    seconds = []
    for t in range(ground_data.shape[0]):
        hrs_in_sec = int(ground_data['time'][t][0:2])*3600
        min_in_sec = int(ground_data['time'][t][3:5])*60
        sec = int(ground_data['time'][t][6:8])
        seconds.append(hrs_in_sec+min_in_sec+sec)
    ground_data['time'] = seconds
    
    min_time = max([ross_data['time'].min(),schmale_data['time'].min(),ground_data['time'].min()])
    max_time = min([ross_data['time'].max(),schmale_data['time'].max(),ground_data['time'].max()])
    
    if min_time>max_time:
        print('NO!')
        break

    ross_data=ross_data[min_time<=ross_data['time']]
    ross_data=ross_data[ross_data['time']<=max_time]
    
    schmale_data=schmale_data[min_time<=schmale_data['time']]
    schmale_data=schmale_data[schmale_data['time']<=max_time]
    
    ground_data=ground_data[min_time<=ground_data['time']]
    ground_data=ground_data[ground_data['time']<=max_time]
    points = [(ross_pos_m[0],ross_pos_m[1]),(schmale_pos_m[0],schmale_pos_m[1]),(ground_m[0],ground_m[1])]
    
    for t in range(ground_data.shape[0]):
        if ground_data.iloc[t]['time'] != schmale_data.iloc[t]['time'] or ground_data.iloc[t]['time'] != ross_data.iloc[t]['time']:
            print('ERROR: Sample Time Inequal @ {0}'.format(t))
            break
        values = [ross_data.iloc[t]['wind_speed'],schmale_data.iloc[t]['wind_speed'],ground_data.iloc[t]['wind_speed']]
        wind_speed = griddata(points,values,(ground_m[0],schmale_pos_m[1]),method='cubic')
        
        plt_sec_temp.append(ground_data.iloc[t]['time'])
        speed_temp.append(wind_speed)
    
    plt_sec.append(plt_sec_temp)
    speed.append(speed_temp)
    

height = 8
width = height*1.61803398875
plt.close('all')
plt.figure(1,figsize=(width,height))
plt.plot(wrf_time,speed_plot,linewidth=3)
for x,y in zip(plt_sec,speed):
    x=[element/3600 for element in x]
    plt.plot(x,y,linewidth=1)
    y_mean = np.mean(y)
    plt.plot([x[0],x[-1]],[y_mean,y_mean],'k',linewidth=3)
plt.title('Wind speed from WRF overlaid with wind speed from coordinated flights')
plt.xlabel('Hours since 0000hrs Mountain Time, 2018-07-17')
plt.ylabel('sec$^{-1}$')
plt.xlim([12,16])
plt.savefig('speed_colorado_campaign_WRF_2018-07-17.png', transparent=False, bbox_inches='tight',pad_inches=0)

#"""


