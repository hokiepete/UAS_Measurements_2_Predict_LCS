# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 15:19:58 2018

@author: pnola
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')
dx=111
dy=111






th = pd.read_csv('CEN.d02.TH', delim_whitespace=True,header=None,usecols=[2])#,names=['id', 'ts_hour', 'id_tsloc', 'ix', 'iy', 't', 'q', 'u', 'v', 'psfc', 'glw', 'gsw', 'hfx', 'lh', 'tsk', 'tslb', 'rainc', 'rainnc', 'clw'])
ph = pd.read_csv('CEN.d02.PH', delim_whitespace=True,header=None,usecols=[2])#,names=['id', 'ts_hour', 'id_tsloc', 'ix', 'iy', 't', 'q', 'u', 'v', 'psfc', 'glw', 'gsw', 'hfx', 'lh', 'tsk', 'tslb', 'rainc', 'rainnc', 'clw'])

temp = th/((1000/ph)**0.286)-273.15

#np.savez('point_speed_07-17',speed=speed,time=lai_ts['ts_hour']+11,pos=[lai_pos[1],lai_pos[0]])

