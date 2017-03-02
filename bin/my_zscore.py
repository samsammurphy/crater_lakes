#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
my_zscore.py

Created on Wed Mar  1 16:24:20 2017
@author: sam
"""

import pandas as pd
import matplotlib.pylab as plt
from plot_field_time_series import plot_unrest_and_eruptions
#import matplotlib_default_colors as colors

# resample data to within 16 days
from read_excel_files import read_satellite_data
df = read_satellite_data('Yugama').resampled('M')#['1990':'2010']

z_scores = []


# calculate z-score for each month
for month in [1,2,3,4,5,6,7,8,9,10,11,12]:
  data = df[(df.index.month >= month) & (df.index.month < month+1)]
  data_z = (data - data.mean())/data.std()
  z_scores.append(data_z)

# concat z scores and sort chronologically
z = pd.concat(z_scores).sort_index(axis=0)

# resampled data
varname = 'dBT'
s1 = df[varname]
s2 = z[varname]

# plot with two y axes
fig, ax1 = plt.subplots()
fig.set_size_inches(12,4)
ax2 = ax1.twinx()

plot_unrest_and_eruptions(ax1)

ax1.plot(s1,'.-',color='#1f77b4',label=varname)
ax1.set_ylabel(varname)
ax1.set_ylim(-10,10)

ax2.plot(s2,'.-',color='#ff7f03',label='z_score')
ax2.set_ylabel('z score')
ax2.set_ylim(-3,3)
ax1.set_xlim(pd.datetime(1990,1,1),pd.datetime(2010,1,1))

lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc=0)