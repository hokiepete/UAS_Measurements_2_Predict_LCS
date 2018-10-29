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
ground_sec = [x/3600 for x in seconds]


MURC_data = pd.read_csv('MSLOG_20180717_TRIM.csv', sep=',',header=1,usecols={2,19},names=['time_stamp','wind_speed'])
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

    

height = 3
width = 6
#width = height*1.61803398875
plt.close('all')
plt.figure(1,figsize=(width,height))
plt.plot(MURC_sec,MURC_speed,color='C0',label='15m\_Tower\_MURC\_3Dsonic')
plt.plot(ground_sec,ground_speed,color='C1',label='15m\_Tower\_Atmos22')

i=0
for x,y in zip(ross_sec,ross_speed):
    x=[element/3600 for element in x]
    if i == 0:
        plt.plot(x,y,color='k',label='15m\_UAS\_A\_Atmos22',linewidth=1)
        i=1
    else:
        plt.plot(x,y,color='k',label='None',linewidth=1)
hand, labl = plt.gca().get_legend_handles_labels()
handout=[]
lablout=[]
for h,l in zip(hand,labl):
   if not l=='None':
        lablout.append(l)
        handout.append(h)
plt.legend(handout,lablout)
#plt.xlabel('Hours since 0000hrs Mountain Time, 2018-07-17')
plt.ylabel('$^{\circ}$C',**labelfont)
plt.xlim([12,16])
plt.ylim([17,30])
plt.xlabel('Hours Mountain Daylight Time, 07-17-2018',**labelfont)
plt.yticks(**tickfont)
plt.xticks(**tickfont)
plt.savefig('temp_A_colorado_campaign_WRF_07-17-2018.png', transparent=False, bbox_inches='tight',pad_inches=0.02,dpi=300)

'''
for x,y in zip(schmale_sec,schmale_speed):
    x=[element/3600 for element in x]
    plt.plot(x,y)
plt.title('15m\_UAS\_Schmale\_Atmos22',**titlefont,y=0.96)
plt.ylabel('m s$^{-1}$',**labelfont)
plt.xlim([12,16])
plt.ylim([0,10])
plt.yticks(**tickfont)
plt.xticks(**tickfont)
plt.xlabel('Hours since 0000hrs Mountain Time, 07-17-2018',**labelfont)
'''
plt.figure(2,figsize=(width,height))
plt.plot(MURC_sec,MURC_speed,color='C0',label='15m\_Tower\_MURC\_3Dsonic')
plt.plot(ground_sec,ground_speed,color='C1',label='15m\_Tower\_Atmos22')

i=0
for x,y in zip(schmale_sec,schmale_speed):
    x=[element/3600 for element in x]
    if i == 0:
        plt.plot(x,y,color='k',label='15m\_UAS\_B\_Atmos22',linewidth=1)
        i=1
    else:
        plt.plot(x,y,color='k',label='None',linewidth=1)
hand, labl = plt.gca().get_legend_handles_labels()
handout=[]
lablout=[]
for h,l in zip(hand,labl):
   if not l=='None':
        lablout.append(l)
        handout.append(h)
plt.legend(handout,lablout)
#plt.xlabel('Hours since 0000hrs Mountain Time, 2018-07-17')
plt.ylabel('$^{\circ}$C',**labelfont)
plt.xlim([12,16])
plt.ylim([17,30])
plt.xlabel('Hours Mountain Daylight Time, 07-17-2018',**labelfont)
plt.yticks(**tickfont)
plt.xticks(**tickfont)
plt.savefig('temp_B_colorado_campaign_WRF_07-17-2018.png', transparent=False, bbox_inches='tight',pad_inches=0.02,dpi=300)
