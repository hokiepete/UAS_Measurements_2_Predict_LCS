import functions as f
from scipy.interpolate import griddata, RegularGridInterpolator
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from time import gmtime
import matplotlib
matplotlib.rcParams['lines.linewidth']=1
matplotlib.rcParams['text.usetex']=True
matplotlib.rcParams['mathtext.fontset'] = 'cm'
plt.rc('font', **{'family': 'serif', 'serif': ['cmr10']})
titlefont = {'fontsize':10}
labelfont = {'fontsize':10}
tickfont = {'fontsize':8}
plt.close('all')
ticks = [13,14,15,16,17]
xmin=12
xmax=16
ymin=0
ymax=12
FigSize=(6,3)#6*9/16)
plt.figure(1,figsize=FigSize)
proj_center_lat = 37.8
proj_center_lon = -106.15
ground2 = [-106.03917,37.781644]
ground4 = [-106.041412,37.782097]
ground5 = [-106.041504,37.782005]

F = np.load('point_speed_07-17.npz')
point_pos = F['pos']
point_s1 = F['speed']
point_time = F['time']
F.close()

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
dx = ground_m[0] - schmale_pos_m[0]
dy = ground_m[1] - schmale_pos_m[1]

s1=[]
plt_sec=[]
for i, pair in enumerate(paired_flights):
    plt_sec_temp = []
    s1_temp = []
    
    ross_data = pd.read_csv('Ross{:d}_DroneMetData.txt'.format(pair[0]), delim_whitespace=True,header=1,names=['date','time','wind_speed','wind_dir','temp'])
    seconds = []
    for t in range(ross_data.shape[0]):
        hrs_in_sec = int(ross_data['time'][t][0:2])*3600
        min_in_sec = int(ross_data['time'][t][3:5])*60
        sec = int(ross_data['time'][t][6:8])
        seconds.append(hrs_in_sec+min_in_sec+sec)
    ross_data['time'] = seconds
    
    schmale_data = pd.read_csv('Schmale{:d}_DroneMetData.txt'.format(pair[1]), delim_whitespace=True,header=1,names=['date','time','wind_speed','wind_dir','temp'])
    seconds = []
    for t in range(schmale_data.shape[0]):
        hrs_in_sec = int(schmale_data['time'][t][0:2])*3600
        min_in_sec = int(schmale_data['time'][t][3:5])*60
        sec = int(schmale_data['time'][t][6:8])
        seconds.append(hrs_in_sec+min_in_sec+sec)
    schmale_data['time'] = seconds

    ground_data = pd.read_csv('Ground5_MetData.txt', delim_whitespace=True,header=1,names=['date','time','wind_speed','wind_dir','temp'])
    seconds = []
    for t in range(ground_data.shape[0]):
        hrs_in_sec = int(ground_data['time'][t][0:2])*3600
        min_in_sec = int(ground_data['time'][t][3:5])*60
        sec = int(ground_data['time'][t][6:8])
        seconds.append(hrs_in_sec+min_in_sec+sec)
    ground_data['time'] = seconds
    
    min_time = max([ross_data['time'].min(),schmale_data['time'].min(),ground_data['time'].min()])
    max_time = min([ross_data['time'].max(),schmale_data['time'].max(),ground_data['time'].max()])
    
    if min_time>max_time:
        print('NO!')
        break
    ross_data=ross_data[min_time<=ross_data['time']]
    ross_data=ross_data[ross_data['time']<=max_time]
    
    schmale_data=schmale_data[min_time<=schmale_data['time']]
    schmale_data=schmale_data[schmale_data['time']<=max_time]
    
    ground_data=ground_data[min_time<=ground_data['time']]
    ground_data=ground_data[ground_data['time']<=max_time]

    points = [(ross_pos_m[0],ross_pos_m[1]),(schmale_pos_m[0],schmale_pos_m[1]),(ground_m[0],ground_m[1])]
    for t in range(ground_data.shape[0]):
        if ground_data.iloc[t]['time'] != schmale_data.iloc[t]['time'] or ground_data.iloc[t]['time'] != ross_data.iloc[t]['time']:
            print('ERROR: Sample Time Inequal @ {0}'.format(t))
            break
        values = [ross_data.iloc[t]['wind_speed'],schmale_data.iloc[t]['wind_speed'],ground_data.iloc[t]['wind_speed']]
        wind_speed = griddata(points,values,(ground_m[0],schmale_pos_m[1]),method='cubic')
        values = [ross_data.iloc[t]['wind_dir'],schmale_data.iloc[t]['wind_dir'],ground_data.iloc[t]['wind_dir']]
        wind_dir = griddata(points,values,(ground_m[0],schmale_pos_m[1]),method='cubic')

        u = -wind_speed*np.sin(f.deg2rad(wind_dir))
        v = wind_speed*np.cos(f.deg2rad(wind_dir))

        u_schmale = -schmale_data.iloc[t]['wind_speed']*np.sin(f.deg2rad(schmale_data.iloc[t]['wind_dir']))
        v_schmale = schmale_data.iloc[t]['wind_speed']*np.cos(f.deg2rad(schmale_data.iloc[t]['wind_dir']))

        u_ground = -ground_data.iloc[t]['wind_speed']*np.sin(f.deg2rad(ground_data.iloc[t]['wind_dir']))
        v_ground = ground_data.iloc[t]['wind_speed']*np.cos(f.deg2rad(ground_data.iloc[t]['wind_dir']))

        plt_sec_temp.append(ground_data.iloc[t]['time'])
        s1_temp.append(np.sqrt(u**2+v**2))
    
    plt_sec.append(plt_sec_temp)
    s1.append(s1_temp)

plt.plot(point_time,point_s1,color='C0')
for x,y in zip(plt_sec,s1):
    x=[element/3600 for element in x]
    plt.plot(x,y,color='C1')
#plt.title('s$_{1}$ from WRF TS overlaid with s$_{1}$ from drone flights',**titlefont,y=0.96)
#plt.title('07-17-2018',**titlefont)#,y=0.96)
plt.ylim([ymin,ymax])
plt.xlim([xmin,xmax])
plt.ylabel('m s$^{-1}$',**labelfont)
plt.yticks(**tickfont)
plt.xticks(**tickfont)
plt.xlabel('Hours since 0000hrs Mountain Daylight Time, 07-17-2018',**labelfont)

plt.savefig('speed_comparison_colorado_campaign_WRF.png', transparent=False, bbox_inches='tight',pad_inches=0.02,dpi=300)






