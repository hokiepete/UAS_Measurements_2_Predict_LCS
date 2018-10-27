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

titlefont = {'fontsize':10}
labelfont = {'fontsize':10}
tickfont = {'fontsize':8}

plt.close('all')


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
ground_speed = ground_data['temp']
ground_sec = seconds#[x/3600 for x in seconds]



MURC_data = pd.read_csv('MSLOG_20180717_TRIM.csv', sep=',',header=1,usecols={2,19},names=['time_stamp','temperature'])

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
#MURC_sec = [x/3600 for x in seconds]
MURC_data['time_stamp'] = seconds
MURC_data = MURC_data.set_index(['time_stamp'])
MURC_data.index = pd.to_datetime(MURC_data.index, unit='s')
MURC_data = MURC_data.resample(rule='15s').mean()
MURC_sec = np.linspace(28800,61290,MURC_data.size)#/3600
MURC_speed = MURC_data['temperature']


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
    ross_speed.append(ross_data['temp'])
    
    schmale_data = pd.read_csv('Schmale{:d}_DroneMetData.txt'.format(pair[1]), delim_whitespace=True,header=1,names=['date','time','wind_speed','wind_dir','temp'])
    seconds = []
    for t in range(schmale_data.shape[0]):
        hrs_in_sec = int(schmale_data['time'][t][0:2])*3600
        min_in_sec = int(schmale_data['time'][t][3:5])*60
        sec = int(schmale_data['time'][t][6:8])
        seconds.append(hrs_in_sec+min_in_sec+sec)
    schmale_speed.append(schmale_data['temp'])
    schmale_sec.append(seconds)

correlation_data = pd.DataFrame()
for m in range(len(MURC_sec)):
    for g in range(len(ground_sec)):
        if MURC_sec[m]==ground_sec[g]:
            for i in range(4):
                for s in range(len(schmale_sec[i])):
                    for r in range(len(ross_sec[i])):
                        if (ross_sec[i][r]==schmale_sec[i][s]) and (ross_sec[i][r]==MURC_sec[m]):
                            d = {'15m\_Tower\_MURC\_3Dsonic':MURC_speed[m],'15m\_Tower\_Atmos22':ground_speed[g],'15m\_UAS\_A\_Atmos22':ross_speed[i][r],'15m\_UAS\_B\_Atmos22':schmale_speed[i][s]}
                            df = pd.DataFrame(data=d,index=[0])
                            correlation_data=correlation_data.append(df,ignore_index=True)
                            '''
                            if not 'correlation_data' in locals():
                                d = {'murc_speed':MURC_sec[m],'ground_speed':ground_sec[g],'ross_speed':ross_sec[i][r],'schmale_speed':schmale_sec[i][s]}
                                correlation_data = pd.DataFrame(data=d,index=[0])
                            else:
                                d = {'murc_speed':MURC_sec[m],'ground_speed':ground_sec[g],'ross_speed':ross_sec[i][r],'schmale_speed':schmale_sec[i][s]}
                                df = pd.DataFrame(data=d,index=[0])
                                correlation_data.append(df,ignore_index=True)
                            '''
    


correlation_data.corr().to_csv('temp_corr.csv', float_format='%.6f')    