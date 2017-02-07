#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

plot_colorbar_v2.py

Created on Mon Feb  6 19:44:13 2017

@author: sam
"""

from load_atmcorr import chronological_data
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import datetime
import time

# read target data
target = 'Poas'
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

# create image
arr = np.array(list(zip(r,g,b)))
img = []  # repeat over a bunch of 'rows'
for i in range(numdays):
  img.append(arr)

plt.imshow(img)
plt.axis("off")
plt.show()

# plot graph for comparison
plt.xlim(start,stop)

plt.plot(alldays,blue_interp,'b-')
plt.plot(alldays,green_interp,'g-')
plt.plot(alldays,red_interp,'r-')

plt.plot(datetimes,blue,'bo')
plt.plot(datetimes,green,'go')
plt.plot(datetimes,red,'ro')

plt.show()