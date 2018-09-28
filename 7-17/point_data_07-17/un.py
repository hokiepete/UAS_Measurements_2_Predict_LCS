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

lai_pos = [37.785701751708984,-106.047157287597656]
lw1_pos = [37.785701751708984,-106.048416137695312]
lw2_pos = [37.785701751708984,-106.049674987792969]
lw3_pos = [37.785705566406250,-106.050941467285156]
lw4_pos = [37.785705566406250,-106.052200317382812]
le1_pos = [37.785701751708984,-106.045890808105469]
le2_pos = [37.785697937011719,-106.044631958007812]
le3_pos = [37.785697937011719,-106.043373107910156]
le4_pos = [37.785697937011719,-106.042106628417969]
ln1_pos = [37.786697387695312,-106.047157287597656]
ln2_pos = [37.787696838378906,-106.047149658203125]
ln3_pos = [37.788692474365234,-106.047149658203125]
ln4_pos = [37.789688110351562,-106.047149658203125]
ls1_pos = [37.784702301025391,-106.047157287597656]
ls2_pos = [37.783706665039062,-106.047157287597656]
ls3_pos = [37.782711029052734,-106.047157287597656]
ls4_pos = [37.781711578369141,-106.047157287597656]

ground5 = [37.782005,-106.041504]
ground = ground5
ross_lon = np.mean([-106.04076,-106.040763,-106.040762,-106.040762])
ross_lat = np.mean([37.780287,37.780307,37.780398,37.780338])
schmale_lon = np.mean([-106.0422848,-106.0422905,-106.0422956,-106.0422941])
schmale_lat = np.mean([37.78153018,37.78155617,37.78156052,37.78156436])

'''
plt.scatter(lai_pos[1],lai_pos[0],color='green')
plt.scatter(lw1_pos[1],lw1_pos[0],color='green')
plt.scatter(lw2_pos[1],lw2_pos[0],color='green')
plt.scatter(lw3_pos[1],lw3_pos[0],color='green')
plt.scatter(lw4_pos[1],lw4_pos[0],color='green')
plt.scatter(le1_pos[1],le1_pos[0],color='green')
plt.scatter(le2_pos[1],le2_pos[0],color='green')
plt.scatter(le3_pos[1],le3_pos[0],color='green')
plt.scatter(le4_pos[1],le4_pos[0],color='green')
plt.scatter(ln1_pos[1],ln1_pos[0],color='green')
plt.scatter(ln2_pos[1],ln2_pos[0],color='green')
plt.scatter(ln3_pos[1],ln3_pos[0],color='green')
plt.scatter(ln4_pos[1],ln4_pos[0],color='green')
plt.scatter(ls1_pos[1],ls1_pos[0],color='green')
plt.scatter(ls2_pos[1],ls2_pos[0],color='green')
plt.scatter(ls3_pos[1],ls3_pos[0],color='green')
plt.scatter(ls4_pos[1],ls4_pos[0],color='green')

plt.scatter(ross_lon,ross_lat,color='blue')
plt.scatter(schmale_lon,schmale_lat,color='blue')
plt.scatter(ground[1],ground[0],color='brown')

plt.axis('equal')
#'''

lai_ts = pd.read_csv('LAI.d02.TS', delim_whitespace=True,header=0,names=['id', 'ts_hour', 'id_tsloc', 'ix', 'iy', 't', 'q', 'u', 'v', 'psfc', 'glw', 'gsw', 'hfx', 'lh', 'tsk', 'tslb', 'rainc', 'rainnc', 'clw'])
lw1_ts = pd.read_csv('LW1.d02.TS', delim_whitespace=True,header=0,names=['id', 'ts_hour', 'id_tsloc', 'ix', 'iy', 't', 'q', 'u', 'v', 'psfc', 'glw', 'gsw', 'hfx', 'lh', 'tsk', 'tslb', 'rainc', 'rainnc', 'clw'])
lw2_ts = pd.read_csv('LW2.d02.TS', delim_whitespace=True,header=0,names=['id', 'ts_hour', 'id_tsloc', 'ix', 'iy', 't', 'q', 'u', 'v', 'psfc', 'glw', 'gsw', 'hfx', 'lh', 'tsk', 'tslb', 'rainc', 'rainnc', 'clw'])
lw3_ts = pd.read_csv('LW3.d02.TS', delim_whitespace=True,header=0,names=['id', 'ts_hour', 'id_tsloc', 'ix', 'iy', 't', 'q', 'u', 'v', 'psfc', 'glw', 'gsw', 'hfx', 'lh', 'tsk', 'tslb', 'rainc', 'rainnc', 'clw'])
lw4_ts = pd.read_csv('LW4.d02.TS', delim_whitespace=True,header=0,names=['id', 'ts_hour', 'id_tsloc', 'ix', 'iy', 't', 'q', 'u', 'v', 'psfc', 'glw', 'gsw', 'hfx', 'lh', 'tsk', 'tslb', 'rainc', 'rainnc', 'clw'])
le1_ts = pd.read_csv('LE1.d02.TS', delim_whitespace=True,header=0,names=['id', 'ts_hour', 'id_tsloc', 'ix', 'iy', 't', 'q', 'u', 'v', 'psfc', 'glw', 'gsw', 'hfx', 'lh', 'tsk', 'tslb', 'rainc', 'rainnc', 'clw'])
le2_ts = pd.read_csv('LE2.d02.TS', delim_whitespace=True,header=0,names=['id', 'ts_hour', 'id_tsloc', 'ix', 'iy', 't', 'q', 'u', 'v', 'psfc', 'glw', 'gsw', 'hfx', 'lh', 'tsk', 'tslb', 'rainc', 'rainnc', 'clw'])
le3_ts = pd.read_csv('LE3.d02.TS', delim_whitespace=True,header=0,names=['id', 'ts_hour', 'id_tsloc', 'ix', 'iy', 't', 'q', 'u', 'v', 'psfc', 'glw', 'gsw', 'hfx', 'lh', 'tsk', 'tslb', 'rainc', 'rainnc', 'clw'])
le4_ts = pd.read_csv('LE4.d02.TS', delim_whitespace=True,header=0,names=['id', 'ts_hour', 'id_tsloc', 'ix', 'iy', 't', 'q', 'u', 'v', 'psfc', 'glw', 'gsw', 'hfx', 'lh', 'tsk', 'tslb', 'rainc', 'rainnc', 'clw'])
ln1_ts = pd.read_csv('LN1.d02.TS', delim_whitespace=True,header=0,names=['id', 'ts_hour', 'id_tsloc', 'ix', 'iy', 't', 'q', 'u', 'v', 'psfc', 'glw', 'gsw', 'hfx', 'lh', 'tsk', 'tslb', 'rainc', 'rainnc', 'clw'])
ln2_ts = pd.read_csv('LN2.d02.TS', delim_whitespace=True,header=0,names=['id', 'ts_hour', 'id_tsloc', 'ix', 'iy', 't', 'q', 'u', 'v', 'psfc', 'glw', 'gsw', 'hfx', 'lh', 'tsk', 'tslb', 'rainc', 'rainnc', 'clw'])
ln3_ts = pd.read_csv('LN3.d02.TS', delim_whitespace=True,header=0,names=['id', 'ts_hour', 'id_tsloc', 'ix', 'iy', 't', 'q', 'u', 'v', 'psfc', 'glw', 'gsw', 'hfx', 'lh', 'tsk', 'tslb', 'rainc', 'rainnc', 'clw'])
ln4_ts = pd.read_csv('LN4.d02.TS', delim_whitespace=True,header=0,names=['id', 'ts_hour', 'id_tsloc', 'ix', 'iy', 't', 'q', 'u', 'v', 'psfc', 'glw', 'gsw', 'hfx', 'lh', 'tsk', 'tslb', 'rainc', 'rainnc', 'clw'])
ls1_ts = pd.read_csv('LS1.d02.TS', delim_whitespace=True,header=0,names=['id', 'ts_hour', 'id_tsloc', 'ix', 'iy', 't', 'q', 'u', 'v', 'psfc', 'glw', 'gsw', 'hfx', 'lh', 'tsk', 'tslb', 'rainc', 'rainnc', 'clw'])
ls2_ts = pd.read_csv('LS2.d02.TS', delim_whitespace=True,header=0,names=['id', 'ts_hour', 'id_tsloc', 'ix', 'iy', 't', 'q', 'u', 'v', 'psfc', 'glw', 'gsw', 'hfx', 'lh', 'tsk', 'tslb', 'rainc', 'rainnc', 'clw'])
ls3_ts = pd.read_csv('LS3.d02.TS', delim_whitespace=True,header=0,names=['id', 'ts_hour', 'id_tsloc', 'ix', 'iy', 't', 'q', 'u', 'v', 'psfc', 'glw', 'gsw', 'hfx', 'lh', 'tsk', 'tslb', 'rainc', 'rainnc', 'clw'])
ls4_ts = pd.read_csv('LS4.d02.TS', delim_whitespace=True,header=0,names=['id', 'ts_hour', 'id_tsloc', 'ix', 'iy', 't', 'q', 'u', 'v', 'psfc', 'glw', 'gsw', 'hfx', 'lh', 'tsk', 'tslb', 'rainc', 'rainnc', 'clw'])


dudx = (le1_ts['u']-lw1_ts['u'])/(2*dx)
dvdx = (le1_ts['v']-lw1_ts['v'])/(2*dx)
dudy = (ln1_ts['u']-ls1_ts['u'])/(2*dy)
dvdy = (ln1_ts['v']-ls1_ts['v'])/(2*dy)

s1 = []
for t in range(dudx.size):
    s1.append(np.linalg.eig(0.5*np.array([[dudx[t],dudy[t]],[dvdx[t],dvdy[t]]])+np.array([[dudx[t],dvdx[t]],[dudy[t],dvdy[t]]]))[0].min())

np.savez('point_s1',s1=s1,time=lai_ts['ts_hour'],pos=[lai_pos[1],lai_pos[0]])

'''
lai_uu = pd.read_csv('LAI.d02.UU', delim_whitespace=True,header=0,names=['time','hgt1','hgt2','hgt3','hgt4','hgt5','hgt6','hgt7','hgt8','hgt9','hgt10','hgt11','hgt12','hgt13','hgt14','hgt15','hgt16','hgt17','hgt18','hgt19','hgt20','hgt21','hgt22','hgt23','hgt24','hgt25'])
lai_vv = pd.read_csv('LAI.d02.VV', delim_whitespace=True,header=0,names=['time','hgt1','hgt2','hgt3','hgt4','hgt5','hgt6','hgt7','hgt8','hgt9','hgt10','hgt11','hgt12','hgt13','hgt14','hgt15','hgt16','hgt17','hgt18','hgt19','hgt20','hgt21','hgt22','hgt23','hgt24','hgt25'])
lai_ph = pd.read_csv('LAI.d02.PH', delim_whitespace=True,header=0,names=['time','hgt1','hgt2','hgt3','hgt4','hgt5','hgt6','hgt7','hgt8','hgt9','hgt10','hgt11','hgt12','hgt13','hgt14','hgt15','hgt16','hgt17','hgt18','hgt19','hgt20','hgt21','hgt22','hgt23','hgt24','hgt25'])
lw4_vv = pd.read_csv('LW4.d02.VV', delim_whitespace=True,header=0,names=['time','hgt1','hgt2','hgt3','hgt4','hgt5','hgt6','hgt7','hgt8','hgt9','hgt10','hgt11','hgt12','hgt13','hgt14','hgt15','hgt16','hgt17','hgt18','hgt19','hgt20','hgt21','hgt22','hgt23','hgt24','hgt25'])
#'''