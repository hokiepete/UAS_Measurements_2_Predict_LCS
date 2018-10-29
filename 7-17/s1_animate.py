# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 11:44:54 2018

@author: pnolan86
"""

import numpy as np
import matplotlib.pyplot as plt
from time import gmtime
import matplotlib
matplotlib.rcParams['text.usetex']=True
matplotlib.rcParams['mathtext.fontset'] = 'cm'
plt.rc('font', **{'family': 'serif', 'serif': ['cmr10']})
titlefont = {'fontsize':10}
labelfont = {'fontsize':10}
tickfont = {'fontsize':8}

F = np.load('wrf_les_s1_4_animation0.npz')
wrf_time = F['time']
t0 = gmtime(wrf_time[0]).tm_hour-6
tf = gmtime(wrf_time[-1]).tm_hour-6
wrf_time = np.linspace(t0,tf,wrf_time.shape[0])
lon = F['lon']
lat = F['lat']
x = F['x']
y = F['y']
s1 = F['s1']
F.close()
figwidth = 16
height = 9
FigSize=(figwidth,height)# y.size/x.size*figwidth)
for t in range(wrf_time.size):
    fig = plt.figure(figsize=FigSize)
    plt.pcolormesh(lon,lat,3600*s1[t,:,:],vmin=-150,vmax=50)
    plt.colorbar(label='hr$^{-1}$')
    plt.scatter(-106.041504,37.7815528075,color='red')
    #plt.colorbar()
    hr,minute = np.divmod(wrf_time[t],1)
    plt.title("{0:02d}:{1:02d} MDT, 2018-07-17".format(int(hr),int(round(minute*60))),fontsize=18)
    plt.savefig('WRF-LES_10m_S1_{0:04d}.tif'.format(t), transparent=False, bbox_inches='tight',dpi=400)
    plt.close('all')

