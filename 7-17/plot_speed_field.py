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
F = np.load('wrf_les.npz')
x = F['x']
y = F['y']
wrf_time = F['time']
proj_center_lon = F['proj_center_lon']
proj_center_lat = F['proj_center_lat']
lat = F['lat']
lon = F['lon']
u = F['u']
v = F['v']
F.close()
#time = tt.gmtime(wrf_time[t_step])

s1_wrf = np.sqrt(u**2+v**2)

plt.close('all')
width = 6
height = 6
plt.figure(1,figsize=(width,height))
gs1 = gridspec.GridSpec(2, 1)
gs1.update(hspace=0.1)
#plt.subplot(211)
plt.subplot(gs1[0,0])
t_step = 21
time = tt.gmtime(wrf_time[t_step])
plt.pcolormesh(lon,lat,1*s1_wrf[t_step,:,:],vmin=0,vmax=15)
plt.colorbar(label='hr$^{-1}$')
plt.scatter(-106.041504,37.7815528075,color='red')
plt.title('{0:02d}-{1:02d}-{2:02d}, {3:02d}{4:02d} MDT'.format(time[1],time[2],time[0],time[3]-6,time[4]),**titlefont,y=0.98)
plt.yticks(**tickfont)
plt.xticks([])#**tickfont)
#plt.subplot(212)
plt.subplot(gs1[1,0])
t_step = 24
time = tt.gmtime(wrf_time[t_step])
plt.pcolormesh(lon,lat,1*s1_wrf[t_step,:,:],vmin=0,vmax=15)
plt.colorbar(label='hr$^{-1}$')
plt.scatter(-106.041504,37.7815528075,color='red')
plt.title('{0:02d}-{1:02d}-{2:02d}, {3:02d}{4:02d} MDT'.format(time[1],time[2],time[0],time[3]-6,time[4]),**titlefont,y=0.98)
plt.yticks(**tickfont)
plt.xticks(**tickfont)
plt.savefig('s1_WRF_2018-07-17.png'.format(t_step), transparent=False, bbox_inches='tight',pad_inches=0.02,dpi=300)