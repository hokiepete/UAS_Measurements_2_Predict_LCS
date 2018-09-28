# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 11:44:54 2018

@author: pnolan86
"""

import numpy as np
import matplotlib.pyplot as plt
from time import gmtime

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
figwidth = 8
FigSize=(figwidth, y.size/x.size*figwidth)
for t in range(wrf_time.size):
    fig = plt.figure(figsize=FigSize)
    plt.pcolormesh(lon,lat,s1[t,:,:],vmin=-0.04,vmax=0)
    #plt.colorbar()
    hr,minute = np.divmod(wrf_time[t],1)
    plt.title("{0:02d}:{1:02d} MDT, 2018-07-17".format(int(hr),int(round(minute*60))),fontsize=18)
    plt.savefig('WRF-LES_10m_S1_{0:04d}.tif'.format(t), transparent=False, bbox_inches='tight')
    plt.close('all')
