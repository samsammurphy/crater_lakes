#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cross_correlation_inspect_v3.py

Created on Thu Feb 23 14:28:24 2017
@author: sam
"""

import pandas as pd
import datetime
import math
import time
import numpy as np
import matplotlib.pylab as plt
from scipy import signal


def not_null(df,var_name1,var_name2):
  """
  None null values in both series
  """ 
  # define ok as hue = True (i.e. avoid negative RGBs)
  ok1 = np.array([~pd.isnull(df[var_name1])])[0]
  ok2 = np.array([~pd.isnull(df[var_name2])])[0]
  
  ok = ok1 & ok2
   
  return df[ok]


def interpolate(fs,start,stop,df,varname):
  
  # original data
  actual_time = df['timestamp']
  actual_value = df[varname]
  
  # sampling dates and timestamps
  num_days = (stop-start).days
  num_samples = math.floor(num_days/fs) + 1
  sampling_dates = [start + datetime.timedelta(days=x*fs) for x in range(0,num_samples)]
  sampling_times = [time.mktime(date.timetuple()) for date in sampling_dates]# convert dates to timestamps (i.e. float required for interpolation)
  
  # interpolate
  resampled_value = np.interp(sampling_times, actual_time, actual_value)
  
  return (sampling_dates,resampled_value)

# data frames
target = 'Kelimutu_b'
df = pd.read_excel('/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/data/{0}/{0}_satellite.xlsx'.format(target))

# variable names
var_name1 = 'saturation'
var_name2 = 'value'

# remove null values
df = not_null(df,var_name1,var_name2)

# sampling_frequency (days)
fs = 30

# time period
start = datetime.datetime(1990,1,1)
stop = datetime.datetime(2016,1,1)

# interpolate
dates,var1 = interpolate(fs,start,stop,df,var_name1)
dates,var2 = interpolate(fs,start,stop,df,var_name2)

# auto-correlate
auto = signal.correlate(var1, var1, mode='same')

# cross-correlate
corr = signal.correlate(var1, var2, mode='same')

# normalize
auto /= np.max(auto)
corr /= np.max(corr)
                       
# plot
fig, (ax_var1, ax_var2, ax_corr) = plt.subplots(3, 1, sharex=True)
fig.set_size_inches(12,10)
ax_var1.plot(dates, var1,'.-')
ax_var1.set_ylabel(var_name1)
ax_var2.plot(dates, var2)
ax_var2.set_ylabel(var_name2)
ax_corr.plot(dates, auto)
ax_corr.plot(dates, corr)
ax_corr.set_ylim(-1,1)
ax_corr.set_xlim(start,stop)
ax_corr.plot([min(dates),max(dates)], [0,0],'g--')






# time lag?
time_of_maxcorr = dates[np.where(corr == np.max(corr))[0][0]]
midtime = min(dates) + (max(dates)-min(dates))/2
delay = time_of_maxcorr - midtime
print('var1 is {:.1f} days ahead of var2'.format(delay.days))

# oplot normalized lag adjusted
n1 = var1/np.max(var1)
n2 = var2/np.max(var2)
lagged_dates = [d+delay for d in dates]

fig2, ax = plt.subplots(1,1)
fig2.set_size_inches(12,3)
ax.plot(dates,n1,'-')
ax.plot(lagged_dates,n2,'-')