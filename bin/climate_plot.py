#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

climate_plot.py

Simple examples of some climate plots

Created on Fri Mar  3 12:08:19 2017
@author: sam
"""

import pandas as pd
import matplotlib.pylab as plt
import matplotlib.dates as mdates

def read_climate():
  bpath = '/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/data/Kelimutu/climate/'
  df = pd.read_pickle(bpath+'all_Met_1987_2017.pkl')
  return df

def subplot(ax,df,name):
  ax.plot(df[name])
  ax.set_ylabel(name)
  ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d %M:%H')
  
  
climate = read_climate()

# subplots
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4,1,sharex=True)
fig.set_size_inches(12,10)
subplot(ax1,climate,'temperature')
subplot(ax2,climate,'dew_point')
subplot(ax3,climate,'sea_level_pressure')
subplot(ax4,climate,'wind_speed')


