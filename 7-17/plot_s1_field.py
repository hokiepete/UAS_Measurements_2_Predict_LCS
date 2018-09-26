# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 15:08:26 2018

@author: pnola
"""

import matplotlib.pyplot as plt
import numpy as np
F = np.load('wrf_les_s1.npz')
x = F['x']
y = F['y']
wrf_time = F['time']
proj_center_lon = F['proj_center_lon']
proj_center_lat = F['proj_center_lat']
s1_wrf = F['s1']
F.close()


plt.pcolormesh(x,y,s1_wrf[0,:,:])
plt.colorbar()