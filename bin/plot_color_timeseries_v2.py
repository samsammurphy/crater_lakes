#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

plot_color_timeseries.py


Created on Mon Feb  6 20:26:00 2017
@author: sam
"""


import numpy as np
import datetime
import time
from PIL import Image

def color_metric_timeseries(ax, r,g,b,numrows):
  """
  visualize color metric time series as image
  
  """   
  # 2D wavebands
  R = np.tile(r, (numrows, 1))
  G = np.tile(g, (numrows, 1))
  B = np.tile(b, (numrows, 1))
  
  # 3D 24-bit array
  rgb = np.zeros((numrows, len(r), 3), dtype=np.uint8)
  rgb[..., 0] = R
  rgb[..., 1] = G
  rgb[..., 2] = B
  
  # Show image in axes object
  im = Image.fromarray(rgb)
  ax.imshow(im)
  
 
def plot_color_timeseries(ax, data, start, stop, numrows):
  """
  Plots color of lake through time series
  """
  
  # set time period (x axis)
  ax.set_xlim(start, stop)
   
  r = 
  
  # create higher resolution timestamps
  numdays = (stop-start).days
  samples = range(0, numdays+delta, delta)
  hires_dates = [start + datetime.timedelta(days=x) for x in samples]
  hires_time = [time.mktime(date.timetuple()) for date in hires_dates]

  # interpolate r,g,b for all datetimes
  R = np.interp(hires_time, data['timestamps'], data['r'])
  G = np.interp(hires_time, data['timestamps'], data['g'])
  B = np.interp(hires_time, data['timestamps'], data['b'])
  
  # plot lake color time series
  for i, hidate in enumerate(hires_dates):
    ax.plot([hidate,hidate],[0,1],color=(R[i],G[i],B[i]))
    
  # remove y ticks
  ax.set_yticklabels([])
  ax.set_yticks([])
  
  # label axes
  #ax.set_ylabel('true color')