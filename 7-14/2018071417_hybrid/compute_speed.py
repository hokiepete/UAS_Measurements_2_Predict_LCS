# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 15:19:58 2018

@author: pnola
"""

#from mpl_toolkits.basemap import Basemap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')
dx=111
dy=111


lai_pos = [37.7815,-106.041]
'''
ground5 = [37.782005,-106.041504]
ground = ground5
ross_lon = np.mean([-106.04076,-106.040763,-106.040762,-106.040762])
ross_lat = np.mean([37.780287,37.780307,37.780398,37.780338])
schmale_lon = np.mean([-106.0422848,-106.0422905,-106.0422956,-106.0422941])
schmale_lat = np.mean([37.78153018,37.78155617,37.78156052,37.78156436])


plt.scatter(lai_pos[1],lai_pos[0],color='green')

plt.scatter(ross_lon,ross_lat,color='blue')
plt.scatter(schmale_lon,schmale_lat,color='blue')
plt.scatter(ground[1],ground[0],color='brown')

plt.axis('equal')
#'''
lai_ts = pd.read_csv('CEN.d02.TS', delim_whitespace=True,header=0,names=['id', 'ts_hour', 'id_tsloc', 'ix', 'iy', 't', 'q', 'u', 'v', 'psfc', 'glw', 'gsw', 'hfx', 'lh', 'tsk', 'tslb', 'rainc', 'rainnc', 'clw'])
lw1_ts = pd.read_csv('CW1.d02.TS', delim_whitespace=True,header=0,names=['id', 'ts_hour', 'id_tsloc', 'ix', 'iy', 't', 'q', 'u', 'v', 'psfc', 'glw', 'gsw', 'hfx', 'lh', 'tsk', 'tslb', 'rainc', 'rainnc', 'clw'])
le1_ts = pd.read_csv('CE1.d02.TS', delim_whitespace=True,header=0,names=['id', 'ts_hour', 'id_tsloc', 'ix', 'iy', 't', 'q', 'u', 'v', 'psfc', 'glw', 'gsw', 'hfx', 'lh', 'tsk', 'tslb', 'rainc', 'rainnc', 'clw'])
ln1_ts = pd.read_csv('CN1.d02.TS', delim_whitespace=True,header=0,names=['id', 'ts_hour', 'id_tsloc', 'ix', 'iy', 't', 'q', 'u', 'v', 'psfc', 'glw', 'gsw', 'hfx', 'lh', 'tsk', 'tslb', 'rainc', 'rainnc', 'clw'])
ls1_ts = pd.read_csv('CS1.d02.TS', delim_whitespace=True,header=0,names=['id', 'ts_hour', 'id_tsloc', 'ix', 'iy', 't', 'q', 'u', 'v', 'psfc', 'glw', 'gsw', 'hfx', 'lh', 'tsk', 'tslb', 'rainc', 'rainnc', 'clw'])


dudx = (le1_ts['u']-lw1_ts['u'])/(2*dx)
dvdx = (le1_ts['v']-lw1_ts['v'])/(2*dx)
dudy = (ln1_ts['u']-ls1_ts['u'])/(2*dy)
dvdy = (ln1_ts['v']-ls1_ts['v'])/(2*dy)

speed = np.sqrt(lai_ts['u']**2+lai_ts['v']**2)
#s1 = []
#for t in range(dudx.size):
#    s1.append(np.linalg.eig(0.5*np.array([[dudx[t],dudy[t]],[dvdx[t],dvdy[t]]])+np.array([[dudx[t],dvdx[t]],[dudy[t],dvdy[t]]]))[0].min())

np.savez('point_speed_07-14',speed=speed,time=lai_ts['ts_hour']+11,pos=[lai_pos[1],lai_pos[0]])

'''
lai_uu = pd.read_csv('LAI.d02.UU', delim_whitespace=True,header=0,names=['time','hgt1','hgt2','hgt3','hgt4','hgt5','hgt6','hgt7','hgt8','hgt9','hgt10','hgt11','hgt12','hgt13','hgt14','hgt15','hgt16','hgt17','hgt18','hgt19','hgt20','hgt21','hgt22','hgt23','hgt24','hgt25'])
lai_vv = pd.read_csv('LAI.d02.VV', delim_whitespace=True,header=0,names=['time','hgt1','hgt2','hgt3','hgt4','hgt5','hgt6','hgt7','hgt8','hgt9','hgt10','hgt11','hgt12','hgt13','hgt14','hgt15','hgt16','hgt17','hgt18','hgt19','hgt20','hgt21','hgt22','hgt23','hgt24','hgt25'])
lai_ph = pd.read_csv('LAI.d02.PH', delim_whitespace=True,header=0,names=['time','hgt1','hgt2','hgt3','hgt4','hgt5','hgt6','hgt7','hgt8','hgt9','hgt10','hgt11','hgt12','hgt13','hgt14','hgt15','hgt16','hgt17','hgt18','hgt19','hgt20','hgt21','hgt22','hgt23','hgt24','hgt25'])
lw4_vv = pd.read_csv('LW4.d02.VV', delim_whitespace=True,header=0,names=['time','hgt1','hgt2','hgt3','hgt4','hgt5','hgt6','hgt7','hgt8','hgt9','hgt10','hgt11','hgt12','hgt13','hgt14','hgt15','hgt16','hgt17','hgt18','hgt19','hgt20','hgt21','hgt22','hgt23','hgt24','hgt25'])
#'''