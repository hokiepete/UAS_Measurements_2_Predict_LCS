# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 14:48:17 2018

@author: pnolan86
"""

from os import listdir
from netCDF4 import Dataset
import numpy as np
files = listdir('wrf_les/')
xdim = 1008
ydim = 882
zdim = 20
height_level = 1
time = np.empty([len(files)])
u = np.empty([len(files),ydim,xdim])
v = np.empty([len(files),ydim,xdim])

tt=0
print(tt)
ncfile='wrf_les/'+files[tt]
root = Dataset(ncfile,'r') #read the data
vars = root.variables #dictionary, all variables in dataset
x = vars['x0'][:]*1000
y = vars['y0'][:]*1000
z = vars['z1'][:]*1000
lon = vars['lon0'][:]
lat = vars['lat0'][:]
proj_center_lon = getattr(vars['grid_mapping_0'],'longitude_of_projection_origin')
proj_center_lat = getattr(vars['grid_mapping_0'],'latitude_of_projection_origin')
time[tt] = vars['time'][:]
u[tt,:,:] = vars['UGRD_HTGL'][0,height_level,:,:].squeeze()
v[tt,:,:] = vars['VGRD_HTGL'][0,height_level,:,:].squeeze()

for tt in range(1,len(files)):
    print(tt)
    ncfile='wrf_les/'+files[tt]
    root = Dataset(ncfile,'r') #read the data
    vars = root.variables #dictionary, all variables in dataset
    time[tt] = vars['time'][:]
    u[tt,:,:] = vars['UGRD_HTGL'][0,height_level,:,:].squeeze()
    v[tt,:,:] = vars['VGRD_HTGL'][0,height_level,:,:].squeeze()

    
print('save')
np.savez('wrf_les_4_animation'+str(height_level)+'.npz',time=time,x=x,y=y,lon=lon,lat=lat,proj_center_lon=proj_center_lon,proj_center_lat=proj_center_lat,u=u,v=v)        
