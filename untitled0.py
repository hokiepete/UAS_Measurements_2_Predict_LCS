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
ground = [-106.03917,37.781644]

'''
flights (4,4) were on a different day from the rest
ross_lon = [-106.040772,-106.04076,-106.040763,-106.040762,-106.040762]
ross_lat = [37.780315,37.780287,37.780307,37.780398,37.780338]

schmale_lon = [-106.0422978,-106.0422848,-106.0422905,-106.0422956,-106.0422941]
schmale_lat = [37.78155488,37.78153018,37.78155617,37.78156052,37.78156436]
#(ross, schmale)
paired_flights = [(4,4),(22,9),(23,10),(25,11),(26,12)]
'''

ross_lon = [-106.04076,-106.040763,-106.040762,-106.040762]
ross_lat = [37.780287,37.780307,37.780398,37.780338]

schmale_lon = [-106.0422848,-106.0422905,-106.0422956,-106.0422941]
schmale_lat = [37.78153018,37.78155617,37.78156052,37.78156436]
#(ross, schmale)
paired_flights = [(22,9),(23,10),(25,11),(26,12)]
#paired_flights = [(22,9),(23,10),(26,12)]

s1=[]
plt_sec=[]
for i, pair in enumerate(paired_flights):
    '''
    if i == 2:
        continue
    '''
    plt_sec_temp = []
    s1_temp = []
    ross_pos_km = f.lonlat2m(ground[0],ground[1],ross_lon[i],ross_lat[i])
    schmale_pos_km = f.lonlat2m(ground[0],ground[1],schmale_lon[i],schmale_lat[i])
    ground_km = [0,0]
    dx=ross_pos_km[0]-schmale_pos_km[0]
    dy=schmale_pos_km[1]-ross_pos_km[1]
    #print('dx = '+str(dx),'dy = '+str(dy))
    
    
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
        #break
    #print([x for x in ground_data['time'] if min_time < x and x < max_time])
    ross_data=ross_data[min_time<=ross_data['time']]
    ross_data=ross_data[ross_data['time']<=max_time]
    
    schmale_data=schmale_data[min_time<=schmale_data['time']]
    schmale_data=schmale_data[schmale_data['time']<=max_time]
    
    ground_data=ground_data[min_time<=ground_data['time']]
    ground_data=ground_data[ground_data['time']<=max_time]
    #s1=[]
    points = [(ross_pos_km[0],ross_pos_km[1]),(schmale_pos_km[0],schmale_pos_km[1]),(ground_km[0],ground_km[1])]
    for t in range(ground_data.shape[0]):
        if ground_data.iloc[t]['time'] != schmale_data.iloc[t]['time'] or ground_data.iloc[t]['time'] != ross_data.iloc[t]['time']:
            print('ERROR: Sample Time Inequal @ {0}'.format(t))
            break
        values = [ross_data.iloc[t]['wind_speed'],schmale_data.iloc[t]['wind_speed'],ground_data.iloc[t]['wind_speed']]
        wind_speed = griddata(points,values,(ross_pos_km[0],schmale_pos_km[1]),method='cubic')
        values = [ross_data.iloc[t]['wind_dir'],schmale_data.iloc[t]['wind_dir'],ground_data.iloc[t]['wind_dir']]
        wind_dir = griddata(points,values,(ross_pos_km[0],schmale_pos_km[1]),method='cubic')
        u = wind_speed*np.cos(wind_dir)
        v = wind_speed*np.sin(wind_dir)
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
for x,y in zip(plt_sec,s1):
    x=[element/3600 for element in x]
    plt.plot(x,y,linewidth=1)
    y_mean = np.mean(y)
    plt.plot([x[0],x[-1]],[y_mean,y_mean],'k',linewidth=3)

#plt.plot(plt_sec,s1)
plt.title('s$_{1}$ from coordinated flights')
plt.xlabel('Hours since 0000hrs Mountain Time, 2018-07-17')
plt.ylabel('sec$^{-1}$')
plt.savefig('s1_colorado_campaign_2018-07-17.png', transparent=False, bbox_inches='tight',pad_inches=0)

#"""


