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
#import time as t_func
from time import gmtime
import matplotlib
matplotlib.rcParams['text.usetex']=True
matplotlib.rcParams['mathtext.fontset'] = 'cm'
plt.rc('font', **{'family': 'serif', 'serif': ['cmr10']})
titlefont = {'fontsize':10}
labelfont = {'fontsize':10}
tickfont = {'fontsize':8}
plt.close('all')

F = np.load('wrf_les_s1.npz')
x = F['x']
y = F['y']
wrf_time = F['time']
t0 = gmtime(wrf_time[0]).tm_hour-6
tf = gmtime(wrf_time[-1]).tm_hour-6
wrf_time = np.linspace(t0,tf,wrf_time.shape[0])
proj_center_lon = F['proj_center_lon']
proj_center_lat = F['proj_center_lat']
s1_wrf = 3600*F['s1']
F.close()
'''
F = np.load('point_s1.npz')
point_pos = F['pos']
point_s1 = 3600*F['s1']
point_time = F['time']
F.close()
'''
ground2 = [-106.03917,37.781644]
ground5 = [-106.041504,37.782005]
ground = ground2

ross_lon = np.mean([-106.040772,-106.040763])
ross_lat = np.mean([37.780315,37.780312])


schmale_lon = np.mean([-106.0422978,-106.0422984])
schmale_lat = np.mean([37.78155488	,37.7815583])

#(ross, schmale)
paired_flights = [(4,4),(5,5)]
plt.scatter(ground[0],ground[1],color='brown')
plt.scatter(ross_lon,ross_lat,color='blue')
plt.scatter(schmale_lon,schmale_lat,color='red')

'''
plt.scatter(ground[0],ground[1],color='brown')
plt.scatter(ross_lon[0],ross_lat[0],color='blue')
plt.scatter(ross_lon[1],ross_lat[1],color='blue')
plt.scatter(schmale_lon[0],schmale_lat[0],color='red')
plt.scatter(schmale_lon[1],schmale_lat[1],color='red')
'''
ground_m = f.lonlat2m(proj_center_lon,proj_center_lat,ground[0],ground[1])
ross_pos_m = f.lonlat2m(proj_center_lon,proj_center_lat,ross_lon,ross_lat)
schmale_pos_m = f.lonlat2m(proj_center_lon,proj_center_lat,schmale_lon,schmale_lat)
dx = ross_pos_m[0] - schmale_pos_m[0]
dy = schmale_pos_m[1] - ross_pos_m[1]

points = (wrf_time,y,x)
[yi,zi,xi] = np.meshgrid(schmale_pos_m[1],wrf_time,ross_pos_m[0])
Xi = (zi.ravel(),yi.ravel(),xi.ravel())
fs1 = RegularGridInterpolator(points,s1_wrf)
s1_plot = fs1(Xi)

[yi,zi,xi] = np.meshgrid(schmale_pos_m[1],wrf_time,schmale_pos_m[0])
Xi = (zi.ravel(),yi.ravel(),xi.ravel())
fs1 = RegularGridInterpolator(points,s1_wrf,method='nearest')
schmale_s1_plot = fs1(Xi)

[yi,zi,xi] = np.meshgrid(ross_pos_m[1],wrf_time,ross_pos_m[0])
Xi = (zi.ravel(),yi.ravel(),xi.ravel())
fs1 = RegularGridInterpolator(points,s1_wrf,method='nearest')
ross_s1_plot = fs1(Xi)

[yi,zi,xi] = np.meshgrid(ground_m[1],wrf_time,ground_m[0])
Xi = (zi.ravel(),yi.ravel(),xi.ravel())
fs1 = RegularGridInterpolator(points,s1_wrf,method='nearest')
ground_s1_plot = fs1(Xi)


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

    ground_data = pd.read_csv('Ground2_MetData.txt', delim_whitespace=True,header=1,names=['date','time','wind_speed','wind_dir','temp'])
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
        wind_speed = griddata(points,values,(ross_pos_m[0],schmale_pos_m[1]),method='cubic')
        values = [ross_data.iloc[t]['wind_dir'],schmale_data.iloc[t]['wind_dir'],ground_data.iloc[t]['wind_dir']]
        wind_dir = griddata(points,values,(ross_pos_m[0],schmale_pos_m[1]),method='cubic')

        u = -wind_speed*np.sin(f.deg2rad(wind_dir))
        v = wind_speed*np.cos(f.deg2rad(wind_dir))

        u_schmale = -schmale_data.iloc[t]['wind_speed']*np.sin(f.deg2rad(schmale_data.iloc[t]['wind_dir']))
        v_schmale = schmale_data.iloc[t]['wind_speed']*np.cos(f.deg2rad(schmale_data.iloc[t]['wind_dir']))
        
        u_ross = -ross_data.iloc[t]['wind_speed']*np.sin(f.deg2rad(ross_data.iloc[t]['wind_dir']))
        v_ross = ross_data.iloc[t]['wind_speed']*np.cos(f.deg2rad(ross_data.iloc[t]['wind_dir']))

        u_ground = -ground_data.iloc[t]['wind_speed']*np.sin(f.deg2rad(ground_data.iloc[t]['wind_dir']))
        v_ground = ground_data.iloc[t]['wind_speed']*np.cos(f.deg2rad(ground_data.iloc[t]['wind_dir']))

        dudx = (u-u_schmale)/dx
        dudy = (u-u_ross)/dy
        dvdx = (v-v_schmale)/dx
        dvdy = (v-v_ross)/dy
        
        J = np.array([[dudx,dudy],[dvdx,dvdy]])
        S = 0.5*(J+J.T)
        plt_sec_temp.append(ground_data.iloc[t]['time'])
        s1_temp.append(3600*np.linalg.eig(S)[0].min())
    
    plt_sec.append(plt_sec_temp)
    s1.append(s1_temp)
    

height = 8.5
width = 6

plt.figure(1,figsize=(width,height))

plt.subplot(411)
plt.plot(wrf_time,s1_plot)
for x,y in zip(plt_sec,s1):
    x=[element/3600 for element in x]
    plt.plot(x,y)
plt.title('s$_{1}$ linearly interpolated from WRF overlaid with s$_{1}$ from drone flights',**titlefont,y=0.96)
plt.ylabel('hr$^{-1}$',**labelfont)
#plt.xlim([12,16])
plt.ylim([-288,72])
plt.xticks([])
plt.yticks(**tickfont)
#plt.xlabel('Housrs since 0000hrs Mountain Time, 2018-07-17')

plt.subplot(412)
plt.plot(wrf_time,schmale_s1_plot)
for x,y in zip(plt_sec,s1):
    x=[element/3600 for element in x]
    plt.plot(x,y)
plt.title('s$_{1}$ from WRF nearest Schmale drone overlaid with s$_{1}$ from drone flights',**titlefont,y=0.96)
plt.ylabel('hr$^{-1}$',**labelfont)
#plt.xlim([12,16])
plt.ylim([-288,72])
plt.xticks([])
plt.yticks(**tickfont)

plt.subplot(413)
plt.plot(wrf_time,ross_s1_plot)
for x,y in zip(plt_sec,s1):
    x=[element/3600 for element in x]
    plt.plot(x,y)
plt.title('s$_{1}$ from WRF nearest Ross drone overlaid with s$_{1}$ from drone flights',**titlefont,y=0.96)
plt.ylabel('hr$^{-1}$',**labelfont)
plt.ylim([-288,72])
#plt.xlim([12,16])
plt.xticks([])
plt.yticks(**tickfont)

plt.subplot(414)
plt.plot(wrf_time,ground_s1_plot)
for x,y in zip(plt_sec,s1):
    x=[element/3600 for element in x]
    plt.plot(x,y)
plt.title('s$_{1}$ from WRF nearest MURC overlaid with s$_{1}$ from drone flights',**titlefont,y=0.96)
plt.ylim([-288,72])
#plt.xlim([12,16])
plt.ylabel('hr$^{-1}$',**labelfont)
plt.xticks(**tickfont)
plt.yticks(**tickfont)
'''
plt.subplot(515)
plt.plot(point_time,point_s1)
for x,y in zip(plt_sec,s1):
    x=[element/3600 for element in x]
    plt.plot(x,y)
plt.title('s$_{1}$ from WRF TS overlaid with s$_{1}$ from drone flights',**titlefont,y=0.96)
plt.ylim([-288,72])
plt.xlim([12,16])
plt.ylabel('hr$^{-1}$',**labelfont)
plt.yticks(**tickfont)
plt.xticks([12,13,14,15,16],**tickfont)
plt.xlabel('Hours since 0000hrs Mountain Time, 2018-07-17',**labelfont)
'''
plt.savefig('s1_comparison_colorado_campaign_WRF_2018-07-14.png', transparent=False, bbox_inches='tight',pad_inches=0.02,dpi=300)
