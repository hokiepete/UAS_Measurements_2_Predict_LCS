# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 19:34:10 2016

@author: pnolan86

source: https://www.youtube.com/watch?v=mlAuOKD1ff8
"""


from os import listdir
from netCDF4 import Dataset
#import numpy as np
files = listdir('wrf_les/')

f = open('NC_MetaData.doc', 'w')
for tt in range(len(files)):
    ncfile='wrf_les/'+files[tt]
    root = Dataset(ncfile,'r') #read the data
    dims = root.dimensions
    vars = root.variables #dictionary, all variables in dataset
    #For each variable query its dimensions and attributes
    for var in vars:
        if var != 'time':
            continue
        f.write("---------- variable "+var+", file "+files[tt]+" ----------\n")
        f.write("shape = "+str(vars[var].shape)+"\n") #dimensions of variable, tuple
        vdims = vars[var].dimensions #vdims is a tuple
        for vd in vdims:
            f.write("dimension["+vd+"] = "+str(len(dims[vd]))+"\n") #f.write length of variable
        vattrs = vars[var].ncattrs() #dictionary
        f.write("number of attributes = "+str(len(vattrs))+"\n")
        for vat in vattrs:
            f.write("attribute["+vat+"] = "+str(getattr(vars[var],vat))+"\n")
        #now just a slice of data
        #a = vars[var][0:23]
        #f.write(a)
    
    root.close()

f.close()


'''
from netCDF4 import Dataset
#import matplotlib.pyplot as plt
import numpy as np
#from mpl_toolkits.basemap import Basemap
f = open('NC_MetaData.doc', 'w')
ncfile='f_00051000.mdv.nc'
#ncfile="hosiendata.nc"
root = Dataset(ncfile,'r') #read the data

#Query number of dimensions
dims = root.dimensions #dictionary
ndims = len(dims) #number of dimensions
f.write("The # of dimensions = "+str(ndims)+"\n")

# f.write the name and length of each dimension
for key in dims:
    f.write("Dimension["+key+"] = "+str(len(dims[key]))+"\n")
    
gattrs = root.ncattrs() #dictionary
ngattrs = len(gattrs) #number of attributes
f.write("The # of attributes = "+str(ngattrs)+"\n")

#f.write Global Attributes
for key in gattrs:
    f.write("Global_Attribute["+key+"] = "+str(getattr(root,key))+"\n")
    #f.write(

vars = root.variables #dictionary, all variables in dataset
nvars = len(vars) #number of variables in dataset
f.write("The # of variables = "+str(nvars)+"\n")

#For each variable query its dimensions and attributes
for var in vars:
    f.write("---------- variable "+var+" ----------\n")
    f.write("shape = "+str(vars[var].shape)+"\n") #dimensions of variable, tuple
    vdims = vars[var].dimensions #vdims is a tuple
    for vd in vdims:
        f.write("dimension["+vd+"] = "+str(len(dims[vd]))+"\n") #f.write length of variable
    vattrs = vars[var].ncattrs() #dictionary
    f.write("number of attributes = "+str(len(vattrs))+"\n")
    for vat in vattrs:
        f.write("attribute["+vat+"] = "+str(getattr(vars[var],vat))+"\n")
    #now just a slice of data
    #a = vars[var][0:23]
    #f.write(a)
f.close()
root.close()
#'''
