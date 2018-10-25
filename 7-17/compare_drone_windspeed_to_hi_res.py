# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 15:19:58 2018

@author: pnola
"""

#from mpl_toolkits.basemap import Basemap
from os import listdir
from netCDF4 import Dataset
import functions as f
from scipy.interpolate import RegularGridInterpolator
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from time import gmtime
import matplotlib
matplotlib.rcParams['lines.linewidth']=1
matplotlib.rcParams['text.usetex']=True
matplotlib.rcParams['mathtext.fontset'] = 'cm'
plt.rc('font', **{'family': 'serif', 'serif': ['cmr10']})

F = np.load('2018071717_hybrid/point_speed_07-17.npz')
point_speed = F['speed']
point_time = F['time']
F.close()
#lai_ts = pd.read_csv('2018071717_hybrid/CEN.d02.TS', delim_whitespace=True,header=0,names=['id', 'ts_hour', 'id_tsloc', 'ix', 'iy', 't', 'q', 'u', 'v', 'psfc', 'glw', 'gsw', 'hfx', 'lh', 'tsk', 'tslb', 'rainc', 'rainnc', 'clw'])


titlefont = {'fontsize':10}
labelfont = {'fontsize':10}
tickfont = {'fontsize':8}

plt.close('all')
files = listdir('wrf_les/')

#speed = np.sqrt(u**2+v**2)

uk_stat_pos = [-106.03917,37.781644]

ground5 = [-106.041504,37.782005]
ground = ground5

ross_lon = np.mean([-106.04076,-106.040763,-106.040762,-106.040762])
ross_lat = np.mean([37.780287,37.780307,37.780398,37.780338])

schmale_lon = np.mean([-106.0422848,-106.0422905,-106.0422956,-106.0422941])
schmale_lat = np.mean([37.78153018,37.78155617,37.78156052,37.78156436])
#(ross, schmale)
paired_flights = [(22,9),(23,10),(25,11),(26,12)]



ground_data = pd.read_csv('Ground5_MetData.txt', delim_whitespace=True,header=1,names=['date','time','wind_speed','wind_dir','temp'])
seconds = []
for t in range(ground_data.shape[0]):
    hrs_in_sec = int(ground_data['time'][t][0:2])*3600
    min_in_sec = int(ground_data['time'][t][3:5])*60
    sec = int(ground_data['time'][t][6:8])
    seconds.append(hrs_in_sec+min_in_sec+sec)
ground_speed = ground_data['wind_speed']
ground_sec = [x/3600 for x in seconds]



MURC_data = pd.read_csv('MSLOG_20180717_TRIM.csv', sep=',',header=1,usecols={2,5},names=['time_stamp','wind_speed'])
seconds = []
for t in range(MURC_data.shape[0]):
    if ':' not in MURC_data['time_stamp'][t][0:2]:
        hrs_in_sec = int(MURC_data['time_stamp'][t][0:2])*3600
        min_in_sec = int(MURC_data['time_stamp'][t][3:5])*60
        sec = int(MURC_data['time_stamp'][t][6:8])
    else:
        hrs_in_sec = int(MURC_data['time_stamp'][t][0:1])*3600
        min_in_sec = int(MURC_data['time_stamp'][t][2:4])*60
        sec = int(MURC_data['time_stamp'][t][5:7])
    seconds.append(hrs_in_sec+min_in_sec+sec)
MURC_sec = [x/3600 for x in seconds]
MURC_speed = MURC_data['wind_speed']

uk_data = pd.read_csv('UK_station.csv', delim_whitespace=False,header=0,names=['date-time','u','v','w','temp'])
seconds = []
for t in range(uk_data.shape[0]):
    hrs_in_sec = int(uk_data['date-time'][t][12:14])*3600
    min_in_sec = int(uk_data['date-time'][t][15:17])*60
    sec = int(uk_data['date-time'][t][18:20])
    seconds.append(hrs_in_sec+min_in_sec+sec)
uk_speed = np.sqrt(uk_data['u']**2+uk_data['v']**2+uk_data['w']**2)
uk_sec = [x/3600 for x in seconds]

ross_speed=[]
ross_sec=[]
schmale_speed=[]
schmale_sec=[]
for i, pair in enumerate(paired_flights):
    ross_data = pd.read_csv('Ross{:d}_DroneMetData.txt'.format(pair[0]), delim_whitespace=True,header=1,names=['date','time','wind_speed','wind_dir','temp'])
    seconds = []
    for t in range(ross_data.shape[0]):
        hrs_in_sec = int(ross_data['time'][t][0:2])*3600
        min_in_sec = int(ross_data['time'][t][3:5])*60
        sec = int(ross_data['time'][t][6:8])
        seconds.append(hrs_in_sec+min_in_sec+sec)
    ross_sec.append(seconds)
    ross_speed.append(ross_data['wind_speed'])
    
    schmale_data = pd.read_csv('Schmale{:d}_DroneMetData.txt'.format(pair[1]), delim_whitespace=True,header=1,names=['date','time','wind_speed','wind_dir','temp'])
    seconds = []
    for t in range(schmale_data.shape[0]):
        hrs_in_sec = int(schmale_data['time'][t][0:2])*3600
        min_in_sec = int(schmale_data['time'][t][3:5])*60
        sec = int(schmale_data['time'][t][6:8])
        seconds.append(hrs_in_sec+min_in_sec+sec)
    schmale_speed.append(schmale_data['wind_speed'])
    schmale_sec.append(seconds)

    

height = 8.5
width = 6
#width = height*1.61803398875
plt.close('all')
plt.figure(1,figsize=(width,height))
plt.subplot(511)
plt.plot(ground_sec,ground_speed,color='C1')
plt.plot(point_time,point_speed,color='C0')
plt.title('15m\_Tower\_Atmos22',**titlefont,y=0.96)
#plt.xlabel('Hours since 0000hrs Mountain Time, 2018-07-17')
plt.ylabel('m s$^{-1}$',**labelfont)
plt.xlim([12,16])
plt.ylim([0,10])
plt.yticks(**tickfont)
plt.xticks([])

plt.subplot(512)
plt.plot(MURC_sec,MURC_speed,color='C1')
plt.plot(point_time,point_speed,color='C0')
plt.title('15m\_Tower\_MURC\_3Dsonic',**titlefont,y=0.96)
#plt.xlabel('Hours since 0000hrs Mountain Time, 2018-07-17')
plt.ylabel('m s$^{-1}$',**labelfont)
plt.xlim([12,16])
plt.ylim([0,10])
plt.yticks(**tickfont)
plt.xticks([])

plt.subplot(513)
plt.plot(uk_sec,uk_speed,color='C1')
plt.plot(point_time,point_speed,color='C0')
plt.title('2m\_Tower\_CSAT3',**titlefont,y=0.96)
#plt.xlabel('Hours since 0000hrs Mountain Time, 2018-07-17')
plt.ylabel('m s$^{-1}$',**labelfont)
plt.xlim([12,16])
plt.ylim([0,10])
plt.yticks(**tickfont)
plt.xticks([])

plt.subplot(514)
plt.plot(point_time,point_speed,color='C0')
for x,y in zip(ross_sec,ross_speed):
    x=[element/3600 for element in x]
    plt.plot(x,y,color='C1')
plt.title('15m\_UAS\_Ross\_Atmos22',**titlefont,y=0.96)
plt.ylabel('m s$^{-1}$',**labelfont)
plt.xlim([12,16])
plt.ylim([0,10])
plt.yticks(**tickfont)
plt.xticks([])

plt.subplot(515)
plt.plot(point_time,point_speed,color='C0')
for x,y in zip(schmale_sec,schmale_speed):
    x=[element/3600 for element in x]
    plt.plot(x,y,color='C1')
plt.title('15m\_UAS\_Schmale\_Atmos22',**titlefont,y=0.96)
plt.ylabel('m s$^{-1}$',**labelfont)
plt.xlim([12,16])
plt.ylim([0,10])
plt.yticks(**tickfont)
plt.xticks(**tickfont)
plt.xlabel('Hours since 0000hrs Mountain Time, 07-17-2018',**labelfont)

plt.savefig('speed_comparison_colorado_campaign_WRF_07-17-2018_hi_res.png', transparent=False, bbox_inches='tight',pad_inches=0.02,dpi=300)
