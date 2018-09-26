# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 11:15:38 2018

@author: pnola
"""

import numpy as np

dx = 111
dy = 111
#F = np.load('wrf_les.npz')
F = np.load('wrf_les_4_animation0.npz')
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

s1 = np.ma.empty([tdim,ydim,xdim])
for tt in {10}:#range(tdim):
    print(tt)
    dudy,dudx = np.gradient(u[tt,:,:],dy,dx,edge_order=2)
    dvdy,dvdx = np.gradient(v[tt,:,:],dy,dx,edge_order=2)
    for i in range(ydim):
        for j in range(xdim):
            if (dudx[i,j] and dudy[i,j] and dvdx[i,j] and dvdy[i,j] and u[tt,i,j] and v[tt,i,j]) is not np.ma.masked:    
                Grad = np.array([[dudx[i, j], dudy[i, j]], [dvdx[i, j], dvdy[i, j]]])
                S = 0.5*(Grad + np.transpose(Grad))
                s1[tt,i,j] = np.min(np.linalg.eig(S)[0])
    
            else:
                s1[tt,i,j] = np.ma.masked
    

#np.savez('wrf_les_s1_4_animation0.npz',s1=s1,time=time,x=x,y=y,lon=lon,lat=lat,proj_center_lon=proj_center_lon,proj_center_lat=proj_center_lat)        
#np.savez('wrf_les_s1.npz',s1=s1,time=time,x=x,y=y,lon=lon,lat=lat,proj_center_lon=proj_center_lon,proj_center_lat=proj_center_lat)        








