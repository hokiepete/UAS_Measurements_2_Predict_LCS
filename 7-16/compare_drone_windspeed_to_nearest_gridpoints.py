# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 15:19:58 2018

@author: pnola
"""

#from mpl_toolkits.basemap import Basemap
from os import listdir
from netCDF4 import Dataset
import functions as f
from scipy.interpolate import RegularGridInterpolator
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from time import gmtime
import matplotlib
matplotlib.rcParams['text.usetex']=True
matplotlib.rcParams['mathtext.fontset'] = 'cm'
plt.rc('font', **{'family': 'serif', 'serif': ['cmr10']})

titlefont = {'fontsize':10}
labelfont = {'fontsize':10}
tickfont = {'fontsize':8}

plt.close('all')
files = listdir('wrf_les/')
interp_method = 'nearest'

xdim = 1008
ydim = 882
zdim = 20
height_level = 0
tdim = len(files)
time = np.empty([tdim])
u = np.empty([tdim,ydim,xdim])
v = np.empty([tdim,ydim,xdim])

tt=0
print(tt)
ncfile='wrf_les/'+files[tt]
root = Dataset(ncfile,'r') #read the data
vars = root.variables #dictionary, all variables in dataset
x = vars['x0'][:]*1000
y = vars['y0'][:]*1000
lon = vars['lon0'][:]
lat = vars['lat0'][:]
proj_center_lon = getattr(vars['grid_mapping_0'],'longitude_of_projection_origin')
proj_center_lat = getattr(vars['grid_mapping_0'],'latitude_of_projection_origin')
time[tt] = vars['time'][:]
u[tt,:,:] = vars['UGRD_HTGL'][0,height_level,:,:].squeeze()
v[tt,:,:] = vars['VGRD_HTGL'][0,height_level,:,:].squeeze()
root.close()

for tt in range(1,tdim):
    print(tt)
    ncfile='wrf_les/'+files[tt]
    root = Dataset(ncfile,'r') #read the data
    vars = root.variables #dictionary, all variables in dataset
    time[tt] = vars['time'][:]
    u[tt,:,:] = vars['UGRD_HTGL'][0,height_level,:,:].squeeze()
    v[tt,:,:] = vars['VGRD_HTGL'][0,height_level,:,:].squeeze()
    root.close()


speed = np.sqrt(u**2+v**2)

del u,v
t0 = gmtime(time[0]).tm_hour-6
tf = gmtime(time[-1]).tm_hour-6
time = np.linspace(t0,tf,time.shape[0])

uk_stat_pos = [-106.03917,37.781644]

ground5 = [-106.041504,37.782005]
ground = ground5

ross_lon = np.mean([-106.04076,-106.040763,-106.040762,-106.040762])
ross_lat = np.mean([37.780287,37.780307,37.780398,37.780338])

schmale_lon = np.mean([-106.0422848,-106.0422905,-106.0422956,-106.0422941])
schmale_lat = np.mean([37.78153018,37.78155617,37.78156052,37.78156436])
#(ross, schmale)
paired_flights = [(22,9),(23,10),(25,11),(26,12)]

ground_m = f.lonlat2m(proj_center_lon,proj_center_lat,ground[0],ground[1])
ross_pos_m = f.lonlat2m(proj_center_lon,proj_center_lat,ross_lon,ross_lat)
schmale_pos_m = f.lonlat2m(proj_center_lon,proj_center_lat,schmale_lon,schmale_lat)
uk_stat_pos_m = f.lonlat2m(proj_center_lon,proj_center_lat,uk_stat_pos[0],uk_stat_pos[1])

points = (time,y,x)
[yi,ti,xi] = np.meshgrid(ross_pos_m[1],time,ross_pos_m[0])
Xi = (ti.ravel(),yi.ravel(),xi.ravel())
fs = RegularGridInterpolator(points,speed,method=interp_method)
ross_comp_speed = fs(Xi)

[yi,ti,xi] = np.meshgrid(schmale_pos_m[1],time,schmale_pos_m[0])
Xi = (ti.ravel(),yi.ravel(),xi.ravel())
fs = RegularGridInterpolator(points,speed,method=interp_method)
schmale_comp_speed = fs(Xi)

[yi,ti,xi] = np.meshgrid(ground_m[1],time,ground_m[0])
Xi = (ti.ravel(),yi.ravel(),xi.ravel())
fs = RegularGridInterpolator(points,speed,method=interp_method)
ground_comp_speed = fs(Xi)

[yi,ti,xi] = np.meshgrid(uk_stat_pos_m[1],time,uk_stat_pos_m[0])
Xi = (ti.ravel(),yi.ravel(),xi.ravel())
fs = RegularGridInterpolator(points,speed,method=interp_method)
uk_comp_speed = fs(Xi)

ground_data = pd.read_csv('Ground5_MetData.txt', delim_whitespace=True,header=1,names=['date','time','wind_speed','wind_dir','temp'])
seconds = []
for t in range(ground_data.shape[0]):
    hrs_in_sec = int(ground_data['time'][t][0:2])*3600
    min_in_sec = int(ground_data['time'][t][3:5])*60
    sec = int(ground_data['time'][t][6:8])
    seconds.append(hrs_in_sec+min_in_sec+sec)
ground_speed = ground_data['wind_speed']
ground_sec = [x/3600 for x in seconds]



#MURC_data = pd.read_csv('MSLOG_20180717_TRIM.csv', sep=',',header=1,names=['sequence_number','date_stamp','time_stamp','time_usecs','node','wind_speed','wind_speed_units','wind_dir','wind_dir_units','u_axis_velocity','u_axis_velocity_units','v_axis_velocity','v_axis_velocity_units','w_axis_velocity','w_axis_velocity_units','pressure','pressure_units','humidity','humidity_units','temperature','temperature_units','dewpoint','dewpoint_units','prt','prt_units','speed_of_sound','speed_of_sound_units','sonic_temperature','sonic_temperature_units','supply_voltage','supply_voltage_units','analog_input_1','analog_input_1_units','analog_input_2','analog_input_2_units','digital_input_1','digital_input_1_units','status','checksum','raw_data','time_stamp','depth','depth_units','rain','rain_units','solar','solar_units','instrument_time_stamp','wind_sensor_status','compass_heading','compass_heading_units','corrected_wind_dir','corrected_wind_dir_units','avg_wind_speed','avg_wind_speed_units','avg_wind_dir','avg_wind_dir_units','gust_wind_speed','gust_wind_speed_units','gust_wind_dir','gust_wind_dir_units','avg_corrected_wind_dir','avg_corrected_wind_dir_units','total_precipitation','total_precipitation_units','precipitation_intensity','precipitation_intensity_units','precipitation_status','pressure_at_level','pressure_at_level_units','pressure_at_station','pressure_at_station_units','absolute_humidity','absolute_humidity_units','corrected_wind_speed','corrected_wind_speed_units','avg_corrected_wind_speed','avg_corrected_wind_speed_units','corrected_gust_direction','corrected_gust_direction_units','corrected_gust_speed','corrected_gust_speed_units','solar_radiation','solar_radiation_units','sunshine_hours','sunshine_hours_units','solar_sensor_status','GPS_location','GPS_heading','GPS_heading_units','GPS_speed_over_ground','GPS_speed_over_ground_units','GPS_sensor_status','QNH_pressure','QNH_pressure_units','avg_wind_speed_2_min','avg_wind_speed_2_min_units','avg_wind_speed_10_min','avg_wind_speed_10_min_units','avg_wind_dir_2_min','avg_wind_dir_2_min_units','avg_wind_dir_10_min','avg_wind_dir_10_min_units','wind_chill','wind_chill_units','heat_index','heat_index_units','air_density','air_density_units','wet_bulb_temperature','wet_bulb_temperature_units','sunrise_time','solar_noon_time','sunset_time	position_sun','twilight_civil','twilight_nautical','twilight_astronomical','x_tilt','x_tilt_units','y_tilt','y_tilt_units','z_orientation','z_orientation_units','user_information_field'])

MURC_data = pd.read_csv('MSLOG_20180717_TRIM.csv', sep=',',header=1,usecols={2,5},names=['time_stamp','wind_speed'])
seconds = []
for t in range(MURC_data.shape[0]):
    if ':' not in MURC_data['time_stamp'][t][0:2]:
        hrs_in_sec = int(MURC_data['time_stamp'][t][0:2])*3600
        min_in_sec = int(MURC_data['time_stamp'][t][3:5])*60
        sec = int(MURC_data['time_stamp'][t][6:8])
    else:
        hrs_in_sec = int(MURC_data['time_stamp'][t][0:1])*3600
        min_in_sec = int(MURC_data['time_stamp'][t][2:4])*60
        sec = int(MURC_data['time_stamp'][t][5:7])
    seconds.append(hrs_in_sec+min_in_sec+sec)
MURC_sec = [x/3600 for x in seconds]
MURC_speed = MURC_data['wind_speed']

uk_data = pd.read_csv('UK_station.csv', delim_whitespace=False,header=0,names=['date-time','u','v','w','temp'])
seconds = []
for t in range(uk_data.shape[0]):
    hrs_in_sec = int(uk_data['date-time'][t][12:14])*3600
    min_in_sec = int(uk_data['date-time'][t][15:17])*60
    sec = int(uk_data['date-time'][t][18:20])
    seconds.append(hrs_in_sec+min_in_sec+sec)
uk_speed = np.sqrt(uk_data['u']**2+uk_data['v']**2+uk_data['w']**2)
uk_sec = [x/3600 for x in seconds]

ross_speed=[]
ross_sec=[]
schmale_speed=[]
schmale_sec=[]
for i, pair in enumerate(paired_flights):
    ross_data = pd.read_csv('Ross{:d}_DroneMetData.txt'.format(pair[0]), delim_whitespace=True,header=1,names=['date','time','wind_speed','wind_dir','temp'])
    seconds = []
    for t in range(ross_data.shape[0]):
        hrs_in_sec = int(ross_data['time'][t][0:2])*3600
        min_in_sec = int(ross_data['time'][t][3:5])*60
        sec = int(ross_data['time'][t][6:8])
        seconds.append(hrs_in_sec+min_in_sec+sec)
    ross_sec.append(seconds)
    ross_speed.append(ross_data['wind_speed'])
    
    schmale_data = pd.read_csv('Schmale{:d}_DroneMetData.txt'.format(pair[1]), delim_whitespace=True,header=1,names=['date','time','wind_speed','wind_dir','temp'])
    seconds = []
    for t in range(schmale_data.shape[0]):
        hrs_in_sec = int(schmale_data['time'][t][0:2])*3600
        min_in_sec = int(schmale_data['time'][t][3:5])*60
        sec = int(schmale_data['time'][t][6:8])
        seconds.append(hrs_in_sec+min_in_sec+sec)
    schmale_speed.append(schmale_data['wind_speed'])
    schmale_sec.append(seconds)

    

height = 8.5
width = 6
#width = height*1.61803398875
plt.close('all')
plt.figure(1,figsize=(width,height))
plt.subplot(511)
plt.plot(ground_sec,ground_speed,color='orange')
plt.plot(time,ground_comp_speed,color='blue')
plt.title('Wind speed from Ground overlaid with wind speed from WRF',**titlefont,y=0.96)
#plt.xlabel('Hours since 0000hrs Mountain Time, 2018-07-17')
plt.ylabel('m/s',**labelfont)
plt.xlim([12,16])
plt.ylim([0,10])
plt.yticks(**tickfont)
plt.xticks([])

plt.subplot(512)
plt.plot(MURC_sec,MURC_speed,color='orange')
plt.plot(time,ground_comp_speed,color='blue')
plt.title('Wind speed from MURC overlaid with wind speed from WRF',**titlefont,y=0.96)
#plt.xlabel('Hours since 0000hrs Mountain Time, 2018-07-17')
plt.ylabel('m/s',**labelfont)
plt.xlim([12,16])
plt.ylim([0,10])
plt.yticks(**tickfont)
plt.xticks([])

plt.subplot(513)
plt.plot(uk_sec,uk_speed,color='orange')
plt.plot(time,uk_comp_speed,color='blue')
plt.title('Wind speed from UK sonic overlaid with wind speed from WRF',**titlefont,y=0.96)
#plt.xlabel('Hours since 0000hrs Mountain Time, 2018-07-17')
plt.ylabel('m/s',**labelfont)
plt.xlim([12,16])
plt.ylim([0,10])
plt.yticks(**tickfont)
plt.xticks([])

plt.subplot(514)
plt.plot(time,ross_comp_speed,color='blue')
for x,y in zip(ross_sec,ross_speed):
    x=[element/3600 for element in x]
    plt.plot(x,y)
plt.title('Wind speed from WRF overlaid with wind speed from ``Ross" flights',**titlefont,y=0.96)
plt.ylabel('m/s',**labelfont)
plt.xlim([12,16])
plt.ylim([0,10])
plt.yticks(**tickfont)
plt.xticks([])

plt.subplot(515)
plt.plot(time,schmale_comp_speed,color='blue')
for x,y in zip(schmale_sec,schmale_speed):
    x=[element/3600 for element in x]
    plt.plot(x,y)
plt.title('Wind speed from WRF overlaid with wind speed from ``Schmale" flights',**titlefont,y=0.96)
plt.ylabel('m/s',**labelfont)
plt.xlim([12,16])
plt.ylim([0,10])
plt.yticks(**tickfont)
plt.xticks(**tickfont)
plt.xlabel('Hours since 0000hrs Mountain Time, 2018-07-17',**labelfont)

plt.savefig('speed_comparison_colorado_campaign_WRF_2018-07-17.png', transparent=False, bbox_inches='tight',pad_inches=0.02,dpi=300)
