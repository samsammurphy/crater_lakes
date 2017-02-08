#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

plot_colorbar_v3.py
Created on Mon Feb  6 20:26:00 2017
@author: sam
"""


import numpy as np
import matplotlib.pyplot as plt
import datetime
import time

 
def plot_color_timeseries(ax, data, start, stop):
  """
  Plots color of lake through time series
  """
  
  # set time period (x axis)
  ax.set_xlim(start, stop)
  
  # set y limit?
  #ax.set_ylim(0,0.6)
  
  # extract r,g,b
  b = [d['sr']['blue'] for d in data]
  g = [d['sr']['green'] for d in data]
  r = [d['sr']['red'] for d in data]
  
  # extract timestamps
  timestamps = [d['timestamp'] for d in data]
  
  # create higher resolution timestamps
  numdays = (stop-start).days
  hires_dates = [start + datetime.timedelta(days=x) for x in range(0, numdays)]
  hires_time = [time.mktime(date.timetuple()) for date in hires_dates]

  # interpolate r,g,b for all datetimes
  B = np.interp(hires_time, timestamps, b)
  G = np.interp(hires_time, timestamps, g)
  R = np.interp(hires_time, timestamps, r)

  # time series plot
  for i, hidate in enumerate(hires_dates):
    ax.plot([hidate,hidate],[0,1],color=(R[i],G[i],B[i]))
  ax.yticks([])
