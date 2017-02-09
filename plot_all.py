#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

plot_all.py

Plots all the output from a Crater Lake target

Created on Mon Feb  6 20:53:54 2017
@author: sam
"""


import os
import matplotlib.pylab as plt
import datetime
import pandas as pd
import numpy as np

from plot_RGB import plot_RGB
from plot_color_timeseries import plot_color_timeseries
from plot_greyness_and_value import plot_greyness_and_value
from plot_dT import plot_dT


def read_csv(target):
  
  try:
    os.chdir('/home/sam/git/crater_lakes/atmcorr/results/'+target)
    
    df = pd.read_csv(target+'.csv')
    
    return {
      'r':np.clip(df.red.values,0,1),
      'g':np.clip(df.green.values,0,1),
      'b':np.clip(df.blue.values,0,1),
      'dT':df.dBT.values,
      'timestamps':df.timestamp.values,
      'datetimes':[datetime.datetime.fromtimestamp(t) for t in df.timestamp.values],    
      'satellites':df.satellite.values
      }
  except:
    print('File IO error for :'+target)
  

target = 'Yugama'

# figure with subplots
fig = plt.figure(figsize=(8,12))
ax1 = fig.add_subplot(4,1,1) # four rows, one column, first plot                   
ax2 = fig.add_subplot(4,1,2) 
ax3 = fig.add_subplot(4,1,3) 
ax4 = fig.add_subplot(4,1,4)

# time period
start = datetime.datetime(1985,1,1)
stop  = datetime.datetime(2016,1,1)   

# load data
data = read_csv(target)

# plot
plot_RGB(ax1, data, start, stop)
plot_color_timeseries(ax2, data, start, stop, 10)
plot_greyness_and_value(ax3, data, start, stop)
plot_dT(ax4, data, start, stop)


outdir = '/home/sam/git/crater_lakes/plots/'+target
if not os.path.exists(outdir):
  os.mkdir(outdir)
os.chdir(outdir)
plt.savefig(target+'.png')
plt.show()
#  plt.close(fig)