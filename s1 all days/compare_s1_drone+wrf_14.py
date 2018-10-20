

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

    ground_data = pd.read_csv('Ground2_MetData.txt', delim_whitespace=True,header=1,names=['date','time','wind_speed','wind_dir','temp'])
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
        wind_speed = griddata(points,values,(ross_pos_m[0],schmale_pos_m[1]),method='cubic')
        values = [ross_data.iloc[t]['wind_dir'],schmale_data.iloc[t]['wind_dir'],ground_data.iloc[t]['wind_dir']]
        wind_dir = griddata(points,values,(ross_pos_m[0],schmale_pos_m[1]),method='cubic')

        u = -wind_speed*np.sin(f.deg2rad(wind_dir))
        v = wind_speed*np.cos(f.deg2rad(wind_dir))

        u_schmale = -schmale_data.iloc[t]['wind_speed']*np.sin(f.deg2rad(schmale_data.iloc[t]['wind_dir']))
        v_schmale = schmale_data.iloc[t]['wind_speed']*np.cos(f.deg2rad(schmale_data.iloc[t]['wind_dir']))
        
        u_ross = -ross_data.iloc[t]['wind_speed']*np.sin(f.deg2rad(ross_data.iloc[t]['wind_dir']))
        v_ross = ross_data.iloc[t]['wind_speed']*np.cos(f.deg2rad(ross_data.iloc[t]['wind_dir']))

        u_ground = -ground_data.iloc[t]['wind_speed']*np.sin(f.deg2rad(ground_data.iloc[t]['wind_dir']))
        v_ground = ground_data.iloc[t]['wind_speed']*np.cos(f.deg2rad(ground_data.iloc[t]['wind_dir']))

        dudx = (u-u_schmale)/dx
        dudy = (u-u_ross)/dy
        dvdx = (v-v_schmale)/dx
        dvdy = (v-v_ross)/dy
        
        J = np.array([[dudx,dudy],[dvdx,dvdy]])
        S = 0.5*(J+J.T)
        plt_sec_temp.append(ground_data.iloc[t]['time'])
        s1_temp.append(3600*np.linalg.eig(S)[0].min())
    
    plt_sec.append(plt_sec_temp)
    s1.append(s1_temp)
    

height = 8.5
width = 6

plt.figure(1,figsize=(width,height))

plt.subplot(411)
plt.plot(wrf_time,s1_plot)
for x,y in zip(plt_sec,s1):
    x=[element/3600 for element in x]
    plt.plot(x,y)
plt.title('s$_{1}$ linearly interpolated from WRF overlaid with s$_{1}$ from drone flights',**titlefont,y=0.96)
plt.ylabel('hr$^{-1}$',**labelfont)
#plt.xlim([12,16])
plt.ylim([-288,72])
plt.xticks([])
plt.yticks(**tickfont)
#plt.xlabel('Housrs since 0000hrs Mountain Time, 2018-07-17')

plt.subplot(412)
plt.plot(wrf_time,schmale_s1_plot)
for x,y in zip(plt_sec,s1):
    x=[element/3600 for element in x]
    plt.plot(x,y)
plt.title('s$_{1}$ from WRF nearest Schmale drone overlaid with s$_{1}$ from drone flights',**titlefont,y=0.96)
plt.ylabel('hr$^{-1}$',**labelfont)
#plt.xlim([12,16])
plt.ylim([-288,72])
plt.xticks([])
plt.yticks(**tickfont)

plt.subplot(413)
plt.plot(wrf_time,ross_s1_plot)
for x,y in zip(plt_sec,s1):
    x=[element/3600 for element in x]
    plt.plot(x,y)
plt.title('s$_{1}$ from WRF nearest Ross drone overlaid with s$_{1}$ from drone flights',**titlefont,y=0.96)
plt.ylabel('hr$^{-1}$',**labelfont)
plt.ylim([-288,72])
#plt.xlim([12,16])
plt.xticks([])
plt.yticks(**tickfont)

plt.subplot(414)
plt.plot(wrf_time,ground_s1_plot)
for x,y in zip(plt_sec,s1):
    x=[element/3600 for element in x]
    plt.plot(x,y)
plt.title('s$_{1}$ from WRF nearest MURC overlaid with s$_{1}$ from drone flights',**titlefont,y=0.96)
plt.ylim([-288,72])
#plt.xlim([12,16])
plt.ylabel('hr$^{-1}$',**labelfont)
plt.xticks(**tickfont)
plt.yticks(**tickfont)
'''
plt.subplot(515)
plt.plot(point_time,point_s1)
for x,y in zip(plt_sec,s1):
    x=[element/3600 for element in x]
    plt.plot(x,y)
plt.title('s$_{1}$ from WRF TS overlaid with s$_{1}$ from drone flights',**titlefont,y=0.96)
plt.ylim([-288,72])
plt.xlim([12,16])
plt.ylabel('hr$^{-1}$',**labelfont)
plt.yticks(**tickfont)
plt.xticks([12,13,14,15,16],**tickfont)
plt.xlabel('Hours since 0000hrs Mountain Time, 2018-07-17',**labelfont)
'''
plt.savefig('s1_comparison_colorado_campaign_WRF_2018-07-14.png', transparent=False, bbox_inches='tight',pad_inches=0.02,dpi=300)
