#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

plot_colorbar_v3.py
Created on Mon Feb  6 20:26:00 2017
@author: sam
"""


from load_atmcorr import chronological_data
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import datetime
import time

# read target data
target = 'Aoba'
data = chronological_data(target)

# extract r,g,b and datetimes
blue = [d['sr']['blue'] for d in data]
green = [d['sr']['green'] for d in data]
red = [d['sr']['red'] for d in data]
timestamps = [d['timestamp'] for d in data]
datetimes = [datetime.datetime.fromtimestamp(t) for t in timestamps]

# define timestamps for each day
start = datetime.datetime(2000,1,1)
stop = datetime.datetime(2016,1,1)
numdays = (stop-start).days
alldays = [start + datetime.timedelta(days=x) for x in range(0, numdays)]
alltimestamps = [time.mktime(date.timetuple()) for date in alldays]

# interpolate r,g,b for all datetimes
b = np.interp(alltimestamps, timestamps, blue)
g = np.interp(alltimestamps, timestamps, green)
r = np.interp(alltimestamps, timestamps, red)

# time series plot
plt.xlim(start,stop)
for i in range(numdays):
  plt.plot([alldays[i],alldays[i]],[0,1],color=(r[i],g[i],b[i]))
plt.yticks([])
plt.show()

# time series plot
plt.xlim(start,stop)
plt.plot(alldays,b,'b-')
plt.plot(alldays,g,'g-')
plt.plot(alldays,r,'r-')

plt.plot(datetimes,blue,'bo')
plt.plot(datetimes,green,'go')
plt.plot(datetimes,red,'ro')
plt.show()