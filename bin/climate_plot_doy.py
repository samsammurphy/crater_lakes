#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

climate_plot_doy.py

plots average climate data for day of year

Created on Fri Mar  3 12:08:19 2017
@author: sam
"""

import pandas as pd
import matplotlib.pylab as plt

def read_climate():
  bpath = '/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/data/Kelimutu/climate/'
  df = pd.read_pickle(bpath+'all_Met_1987_2017.pkl')
  return df

def subplot(ax,df,name):
  ax.plot(pd.np.linspace(1,366,366),df[name])
  ax.set_ylabel(name)
  ax.set_xlim(1,366)
    
# mean for day of year
climate = read_climate()
doy = climate.groupby([climate.index.month, climate.index.day]).mean()

# subplots
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4,1,sharex=True)
fig.set_size_inches(12,10)
subplot(ax1,doy,'temperature')
subplot(ax2,doy,'dew_point')
subplot(ax3,doy,'sea_level_pressure')
subplot(ax4,doy,'wind_speed')
