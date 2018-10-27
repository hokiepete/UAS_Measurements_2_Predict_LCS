# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 15:19:58 2018

@author: pnola
"""

#from mpl_toolkits.basemap import Basemap
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['text.usetex']=True
matplotlib.rcParams['mathtext.fontset'] = 'cm'
plt.rc('font', **{'family': 'serif', 'serif': ['cmr10']})
matplotlib.rcParams['lines.linewidth']=1
titlefont = {'fontsize':10}
labelfont = {'fontsize':10}
tickfont = {'fontsize':8}

uk_data = pd.read_csv('UK_station.csv', delim_whitespace=False,header=0,names=['date-time','u','v','w','temp'])
seconds = []
for t in range(uk_data.shape[0]):
    hrs_in_sec = int(uk_data['date-time'][t][12:14])*3600
    min_in_sec = int(uk_data['date-time'][t][15:17])*60
    sec = int(uk_data['date-time'][t][18:20])
    seconds.append(hrs_in_sec+min_in_sec+sec)
uk_temp = uk_data['temp']
uk_sec = [x/3600 for x in seconds]

uk_tower = pd.read_csv('tower.csv', delim_whitespace=False,header=0,names=['date-time','2m','1.5m','0.75m'])
seconds = []
for t in range(uk_tower.shape[0]):
    hrs_in_sec = int(uk_tower['date-time'][t][12:14])*3600
    min_in_sec = int(uk_tower['date-time'][t][15:17])*60
    sec = int(uk_tower['date-time'][t][18:20])
    seconds.append(hrs_in_sec+min_in_sec+sec)
    
tower_2m = uk_tower['2m']
tower_1_5m = uk_tower['1.5m']
tower_0_75m = uk_tower['0.75m']
tower_sec = [x/3600 for x in seconds]

    
height = 8.5
width = 6
#height = 15
#width = height*1.61803398875
plt.close('all')
plt.figure(1,figsize=(width,height))
plt.subplot(413)
plt.plot(tower_sec,tower_2m)
print(tower_2m.min(),tower_2m.max())
plt.title('2m\_Tower\_Atmos22',**titlefont,y=0.96)
#plt.xlabel('Hours since 0000hrs Mountain Time, 2018-07-17')
plt.ylabel('$^{\circ}$C',**labelfont)
#plt.xlim([12,16])
plt.xlim([0,24])
plt.ylim([7,31])
plt.yticks(**tickfont)
plt.xticks([])

plt.subplot(412)
plt.plot(tower_sec,tower_1_5m)
print(tower_1_5m.min(),tower_1_5m.max())
plt.title('1.5m\_Tower\_Atmos22',**titlefont,y=0.96)
#plt.xlabel('Hours since 0000hrs Mountain Time, 2018-07-17')
plt.ylabel('$^{\circ}$C',**labelfont)
#plt.xlim([12,16])
plt.xlim([0,24])
plt.ylim([7,31])
plt.yticks(**tickfont)
plt.xticks([])

plt.subplot(411)
plt.plot(tower_sec,tower_0_75m)
print(tower_0_75m.min(),tower_0_75m.max())
plt.title('0.75m\_Tower\_Atmos22',**titlefont,y=0.96)
#plt.xlabel('Hours since 0000hrs Mountain Time, 2018-07-17')
plt.ylabel('$^{\circ}$C',**labelfont)
#plt.xlim([12,16])
plt.xlim([0,24])
plt.ylim([7,31])
plt.yticks(**tickfont)
plt.xticks([])

plt.subplot(414)
plt.plot(uk_sec,uk_temp)
print(uk_temp.min(),uk_temp.max())
plt.title('2m\_Tower\_CSAT3',**titlefont,y=0.96)
#plt.xlabel('Hours since 0000hrs Mountain Time, 2018-07-17')
plt.ylabel('$^{\circ}$C',**labelfont)
#plt.xlim([12,16])
plt.xlim([0,24])
plt.ylim([7,31])
plt.yticks(**tickfont)
plt.xticks(**tickfont)
plt.xlabel('Hours since 0000hrs Mountain Daylight Time, 07-17-2018',**labelfont)
plt.savefig('temperature_comparison_tower_vs_sonic_07-17-2018.png', transparent=False, bbox_inches='tight',pad_inches=0.02,dpi=300)

