#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

spectrogram.py

Created on Wed Feb 22 15:15:54 2017
@author: sam
"""

import numpy as np
import pandas as pd
import datetime
import time
from scipy import signal
import matplotlib.pylab as plt


def interpolate(name,df,start,stop):
  """
  Interpolates a time series over daily frequency
  """

  # variable to interpolate over time
  y = np.array(df[name]) 
  
  # define daily timestamsp
  numdays = (stop-start).days
  D = [start + datetime.timedelta(days=x) for x in range(0,numdays)]
  T = [time.mktime(date.timetuple()) for date in D]
  
  # interpolate y
  Y = np.interp(T, np.array(df['timestamp']), y)
  
  return (D, Y)


# load data
target = 'Kelimutu_c'
df = pd.read_excel('/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/data/{0}/{0}_satellite.xlsx'.format(target))

# interpolate time series
start = datetime.datetime(1985,1,1)
stop = datetime.datetime(2016,1,1)
D, Y = interpolate('dBT',df,start,stop)


# plot original time series
plt.plot(df['datetime'],df['dBT'])
plt.show()


f, t, Sxx = signal.spectrogram(Y,100)
plt.pcolormesh(t, f, Sxx)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()