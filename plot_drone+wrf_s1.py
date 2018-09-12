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

F = np.load('wrf_les_s1.npz')
x = F['x']
y = F['y']
wrf_time = F['time']
t0 = t_func.gmtime(wrf_time[0]).tm_hour-6
tf = t_func.gmtime(wrf_time[-1]).tm_hour-6
wrf_time = np.linspace(t0,tf,wrf_time.shape[0])
proj_center_lon = F['proj_center_lon']
proj_center_lat = F['proj_center_lat']
s1_wrf = F['s1']
F.close()
ground = [-106.03917,37.781644]

ross_lon = np.mean([-106.04076,-106.040763,-106.040762,-106.040762])
ross_lat = np.mean([37.780287,37.780307,37.780398,37.780338])

schmale_lon = np.mean([-106.0422848,-106.0422905,-106.0422956,-106.0422941])
schmale_lat = np.mean([37.78153018,37.78155617,37.78156052,37.78156436])
#(ross, schmale)
paired_flights = [(22,9),(23,10),(25,11),(26,12)]

ground_m = f.lonlat2m(proj_center_lon,proj_center_lat,ground[0],ground[1])
ross_pos_m = f.lonlat2m(proj_center_lon,proj_center_lat,ross_lon,ross_lat)
schmale_pos_m = f.lonlat2m(proj_center_lon,proj_center_lat,schmale_lon,schmale_lat)
dx=ross_pos_m[0]-schmale_pos_m[0]
dy=schmale_pos_m[1]-ross_pos_m[1]
points = (wrf_time,y,x)
[yi,zi,xi] = np.meshgrid(schmale_pos_m[1],wrf_time,ross_pos_m[0])
Xi = (zi.ravel(),yi.ravel(),xi.ravel())
fs1 = RegularGridInterpolator(points,s1_wrf)
s1_plot = fs1(Xi)

s1=[]
plt_sec=[]
for i, pair in enumerate(paired_flights):
    plt_sec_temp = []
    s1_temp = []
    
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
        #break
    #print([x for x in ground_data['time'] if min_time < x and x < max_time])
    ross_data=ross_data[min_time<=ross_data['time']]
    ross_data=ross_data[ross_data['time']<=max_time]
    
    schmale_data=schmale_data[min_time<=schmale_data['time']]
    schmale_data=schmale_data[schmale_data['time']<=max_time]
    
    ground_data=ground_data[min_time<=ground_data['time']]
    ground_data=ground_data[ground_data['time']<=max_time]
    #s1=[]
    points = [(ross_pos_m[0],ross_pos_m[1]),(schmale_pos_m[0],schmale_pos_m[1]),(ground_m[0],ground_m[1])]
    for t in range(ground_data.shape[0]):
        if ground_data.iloc[t]['time'] != schmale_data.iloc[t]['time'] or ground_data.iloc[t]['time'] != ross_data.iloc[t]['time']:
            print('ERROR: Sample Time Inequal @ {0}'.format(t))
            break
        values = [ross_data.iloc[t]['wind_speed'],schmale_data.iloc[t]['wind_speed'],ground_data.iloc[t]['wind_speed']]
        wind_speed = griddata(points,values,(ross_pos_m[0],schmale_pos_m[1]),method='cubic')
        values = [ross_data.iloc[t]['wind_dir'],schmale_data.iloc[t]['wind_dir'],ground_data.iloc[t]['wind_dir']]
        wind_dir = griddata(points,values,(ross_pos_m[0],schmale_pos_m[1]),method='cubic')
        u = -wind_speed*np.sin(f.deg2rad(wind_dir))
        v = wind_speed*np.cos(f.deg2rad(wind_dir))
        #u_ground = ground_data.iloc[t]['wind_speed']*np.cos(ground_data.iloc[t]['wind_dir'])
        #v_ground = ground_data.iloc[t]['wind_speed']*np.sin(ground_data.iloc[t]['wind_dir'])
        u_schmale = schmale_data.iloc[t]['wind_speed']*np.cos(schmale_data.iloc[t]['wind_dir'])
        v_schmale = schmale_data.iloc[t]['wind_speed']*np.sin(schmale_data.iloc[t]['wind_dir'])
        u_ross = ross_data.iloc[t]['wind_speed']*np.cos(ross_data.iloc[t]['wind_dir'])
        v_ross = ross_data.iloc[t]['wind_speed']*np.sin(ross_data.iloc[t]['wind_dir'])
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
        plt_sec_temp.append(ground_data.iloc[t]['time'])
        s1_temp.append(np.linalg.eig(S)[0].min())
    
    plt_sec.append(plt_sec_temp)
    s1.append(s1_temp)
    

#hrs, sec = np.divmod(ross_data['time'],3600)
#mins, sec = np.divmod(mins,60)

#plot_time = []
#for t in range(ground_data.shape[0]):
#    plot_time.append(str(hrs[t])+':'+str(mins[t])+':'+str(sec[t]))
#plt.plot(sec,s1)
#sort_index = np.unravel_index(np.argsort(plt_sec),np.shape(plt_sec))
'''
sort_index = np.argsort(plt_sec)
plt_sec = np.array(plt_sec)[sort_index]
s1 = np.array(s1)[sort_index]
'''
height = 8
width = height*1.61803398875
plt.close('all')
plt.figure(1,figsize=(width,height))
plt.plot(wrf_time,s1_plot,linewidth=3)
for x,y in zip(plt_sec,s1):
    x=[element/3600 for element in x]
    plt.plot(x,y,linewidth=1)
    y_mean = np.mean(y)
    plt.plot([x[0],x[-1]],[y_mean,y_mean],'k',linewidth=3)
#plt.plot(plt_sec,s1)
plt.title('s$_{1}$ from WRF overlaid with s$_{1}$ from coordinated flights')
plt.xlabel('Hours since 0000hrs Mountain Time, 2018-07-17')
plt.ylabel('sec$^{-1}$')
plt.xlim([12,16])
plt.savefig('s1_colorado_campaign_WRF_2018-07-17.png', transparent=False, bbox_inches='tight',pad_inches=0)

#"""


