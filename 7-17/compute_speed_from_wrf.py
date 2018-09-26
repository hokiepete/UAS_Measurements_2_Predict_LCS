# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 11:15:38 2018

@author: pnola
"""

import numpy as np

dx = 111
dy = 111
F = np.load('wrf_les.npz')
x = F['x']
y = F['y']
time = F['time']
lon = F['lon']
lat = F['lat']
proj_center_lon = F['proj_center_lon']
proj_center_lat = F['proj_center_lat']
u = F['u']
v = F['v']        
F.close()
J = np.array([[0, 1], [-1, 0]])
tdim = time.shape[0]
xdim = x.shape[0]
ydim = y.shape[0]

speed = np.ma.empty([tdim,ydim,xdim])
for tt in range(tdim):
    print(tt)
    for i in range(ydim):
        for j in range(xdim):
            if (u[tt,i,j] and v[tt,i,j]) is not np.ma.masked:    
                speed[tt,i,j] = np.sqrt(u[tt,i,j]**2 + v[tt,i,j]**2)
    
            else:
                speed[tt,i,j] = np.ma.masked
    


np.savez('wrf_les_speed.npz',speed=speed,time=time,x=x,y=y,lon=lon,lat=lat,proj_center_lon=proj_center_lon,proj_center_lat=proj_center_lat)        








