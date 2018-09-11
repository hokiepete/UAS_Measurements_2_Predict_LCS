# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 14:48:17 2018

@author: pnolan86
"""

from os import listdir
from netCDF4 import Dataset
import numpy as np
from scipy.interpolate import griddata, LinearNDInterpolator, RegularGridInterpolator
files = listdir('wrf_les/')
xdim = 1008
ydim = 882
zdim = 20

time = np.empty([len(files)])
u = np.empty([len(files),zdim,ydim,xdim])
v = np.empty([len(files),zdim,ydim,xdim])

tt=0
ncfile='wrf_les/'+files[tt]
root = Dataset(ncfile,'r') #read the data
vars = root.variables #dictionary, all variables in dataset
x = vars['x0'][:]
y = vars['y0'][:]
z = vars['z1'][:]
lon = vars['lon0'][:]
lat = vars['lat0'][:]
proj_center_lon = getattr(vars['grid_mapping_0'],'longitude_of_projection_origin')
proj_center_lat = getattr(vars['grid_mapping_0'],'latitude_of_projection_origin')
time[tt] = vars['time'][:]
[yy,zz,xx] = np.meshgrid(y,z,x)
[yi,zi,xi] = np.meshgrid(y,[15],x)
points = (zz.ravel(),yy.ravel(),xx.ravel())
#points = (z,y,x)
Xi = (zi.ravel(),yi.ravel(),xi.ravel())
#u[tt,:,:,:] = griddata(points,vars['UGRD_HTGL'][:],Xi)
fu = LinearNDInterpolator(points,vars['UGRD_HTGL'][:].ravel())
uu = fu(Xi)
#uu = griddata(points,vars['UGRD_HTGL'][:].ravel(),Xi)
#v[tt,:,:,:] = vars['VGRD_HTGL'][:]


'''
for tt in range(1,len(files)):
    ncfile='wrf_les/'+files[tt]
    root = Dataset(ncfile,'r') #read the data
    vars = root.variables #dictionary, all variables in dataset
    time[tt] = vars['time'][:]
    u[tt,:,:,:] = vars['UGRD_HTGL'][:]
    v[tt,:,:,:] = vars['VGRD_HTGL'][:]
    
print('save')
np.savez('wrf_les.npz',time=time,x=x,y=y,z=z,lon=lon,lat=lat,proj_center_lon=proj_center_lon,proj_center_lat=proj_center_lat,u=u,v=v)        
'''