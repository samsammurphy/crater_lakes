#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

cross_correlation_inspect_v2.py

Created on Thu Feb 23 12:34:51 2017
@author: sam
"""


import pandas as pd
import datetime
import math
import time
import numpy as np
import matplotlib.pylab as plt
from scipy import signal

def interpolate(fs,start,stop,df):
  
  # original data
  actual_time = df['timestamp']
  actual_value = df['dBT']
  
  # sampling dates and timestamps
  num_days = (stop-start).days
  num_samples = math.floor(num_days/fs) + 1
  sampling_dates = [start + datetime.timedelta(days=x*fs) for x in range(0,num_samples)]
  sampling_times = [time.mktime(date.timetuple()) for date in sampling_dates]# convert dates to timestamps (i.e. float required for interpolation)
  
  # interpolate
  resampled_value = np.interp(sampling_times, actual_time, actual_value)
  
  return (sampling_dates,resampled_value)


# load Kelimutu data sets
target1 = 'Kelimutu_b'
target2 = 'Kelimutu_c'
df1 = pd.read_excel('/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/data/{0}/{0}_satellite.xlsx'.format(target1))
df2 = pd.read_excel('/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/data/{0}/{0}_satellite.xlsx'.format(target2))

# interpolate to the same sampling frequency
fs = 7 # sampling_frequency (days)
start = datetime.datetime(1990,1,1)
stop = datetime.datetime(2016,1,1)
dates,dBT1 = interpolate(fs,start,stop,df1)
dates,dBT2 = interpolate(fs,start,stop,df2) 

# cross-correlate
corr = signal.correlate(dBT1, dBT2, mode='same')
corr /= np.max(corr)
                       
# plot the original signals and their cross-correlation
fig, (ax_dBT1, ax_dBT2, ax_corr) = plt.subplots(3, 1, sharex=True)
fig.set_size_inches(12,10)
ax_dBT1.plot(dates, dBT1)
ax_dBT2.plot(dates, dBT2)
ax_corr.plot(dates, corr)
fig.show()

# full correlation 
#fig2, ax = plt.subplots(1,1)
#fig2.set_size_inches(12,2)
#ax.plot(signal.correlate(dBT1, dBT2, mode='full') / np.max(corr))

# time lag?
time_of_maxcorr = dates[np.where(corr == np.max(corr))[0][0]]
midtime = min(dates) + (max(dates)-min(dates))/2
delay = time_of_maxcorr - midtime
print('var1 is {:.1f} days ahead of var2'.format(delay.days))

# oplot normalized lag adjusted
n1 = dBT1/np.max(dBT1)
n2 = dBT2/np.max(dBT2)
lagged_dates = [d+delay for d in dates]

fig2, ax = plt.subplots(1,1)
fig2.set_size_inches(12,3)
ax.plot(dates,n1,'-')
ax.plot(lagged_dates,n2,'-')

# calculate correlation coefficient