#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

plot_time_series_v6.py

"""

import pandas as pd
import matplotlib.pylab as plt
import matplotlib.dates as mdates


def read_satellite(target): 
  bpath = '/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/data/{0}/{0}'.format(target)
  df = pd.read_excel('{0}_satellite.xlsx'.format(bpath))
  df = df.set_index(pd.DatetimeIndex(df['datetime']))
  return df
  
def read_climate():
  bpath = '/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/data/Kelimutu/climate/'
  df = pd.read_pickle(bpath+'all_Met_1987_2017.pkl')
  return df
     
def subplot(ax,df,name):
  """ simple plot """
  
  ax.plot(df[name])
  ax.set_ylabel(name)
  
  # Make the interactive navigation show high precision datetime
  ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d %M:%H')


# target lake
target = 'Kelimutu_c'

# data
sat = read_satellite(target)#['1990-03-28':'1990-04-01']
climate = read_climate()

# subplots
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4,1,sharex=True)
fig.set_size_inches(6,5)
subplot(ax1,sat,'hue')
subplot(ax2,sat,'saturation')
subplot(ax3,sat,'value')
subplot(ax4,climate,'temperature')
