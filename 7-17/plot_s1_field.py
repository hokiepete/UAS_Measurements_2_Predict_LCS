# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 15:08:26 2018

@author: pnola
"""

import matplotlib.pyplot as plt
import numpy as np
import time as tt
import matplotlib
import matplotlib.gridspec as gridspec
matplotlib.rcParams['text.usetex']=True
matplotlib.rcParams['mathtext.fontset'] = 'cm'
plt.rc('font', **{'family': 'serif', 'serif': ['cmr10']})
titlefont = {'fontsize':10}
labelfont = {'fontsize':10}
tickfont = {'fontsize':8}
#t_step = 24
F = np.load('wrf_les_s1.npz')
x = F['x']
y = F['y']
wrf_time = F['time']
proj_center_lon = F['proj_center_lon']
proj_center_lat = F['proj_center_lat']
lat = F['lat']
lon = F['lon']
s1_wrf = F['s1']
F.close()
#time = tt.gmtime(wrf_time[t_step])


plt.close('all')
width = 6
height = 9/16*width
plt.figure(1,figsize=(width,height))
#gs1 = gridspec.GridSpec(2, 1)
#gs1.update(hspace=0.1)
#plt.subplot(211)
#plt.subplot(gs1[0,0])
t_step = 12
time = tt.gmtime(wrf_time[t_step])
plt.pcolormesh(lon,lat,3600*s1_wrf[t_step,:,:],vmin=-150,vmax=50)
plt.colorbar(label='hr$^{-1}$')
plt.scatter(-106.041504,37.7815528075,color='red')
plt.title('{0:02d}-{1:02d}-{2:02d}, {3:02d}{4:02d} MDT'.format(time[1],time[2],time[0],time[3]-6,time[4]),**titlefont,y=0.98)
plt.yticks(**tickfont)
plt.xticks(**tickfont)
plt.xlabel('$^{\\circ}$ Longitude',**labelfont)
plt.ylabel('$^{\\circ}$ Latitude',**labelfont)
plt.savefig('s1_WRF_2018-07-17_{0}.png'.format(t_step), transparent=False, bbox_inches='tight',pad_inches=0.02,dpi=300)

plt.figure(2,figsize=(width,height))

#plt.subplot(212)
#plt.subplot(gs1[1,0])
t_step = 23
time = tt.gmtime(wrf_time[t_step])
plt.pcolormesh(lon,lat,3600*s1_wrf[t_step,:,:],vmin=-150,vmax=50)
plt.colorbar(label='hr$^{-1}$')
plt.scatter(-106.041504,37.7815528075,color='red')
plt.title('{0:02d}-{1:02d}-{2:02d}, {3:02d}{4:02d} MDT'.format(time[1],time[2],time[0],time[3]-6,time[4]),**titlefont,y=0.98)
plt.yticks(**tickfont)
plt.xticks(**tickfont)
plt.xlabel('$^{\\circ}$ Longitude',**labelfont)
plt.ylabel('$^{\\circ}$ Latitude',**labelfont)
plt.savefig('s1_WRF_2018-07-17_{0}.png'.format(t_step), transparent=False, bbox_inches='tight',pad_inches=0.02,dpi=300)