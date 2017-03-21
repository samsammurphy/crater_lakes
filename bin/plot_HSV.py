#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

plot_HSV.py

"""

import pandas as pd
import matplotlib.pylab as plt
import matplotlib.dates as mdates
import os

def read_excel(target):
  """ read excel file for target """
  
  bpath = '/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/data/{0}/{0}'.format(target)
  fpath = '{0}_satellite.xlsx'.format(bpath)
  df = pd.read_excel(fpath)

  # set datetime as index
  df = df.set_index(pd.DatetimeIndex(df['datetime']))
  
  return df
     
def subplot(ax,df,name):
  """ simple plot """
  
  ax.plot(df[name])
  ax.set_ylabel(name)
  
  # Make the interactive navigation show high precision datetime
  ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d %M:%H')


# target lake
target = 'Kelimutu_c'

# satellite data
df = read_excel(target)#['1990-03-28':'1990-04-01']

# resample and interpolate
#df = df.resample('1D').agg('mean').interpolate(method='time')

# subplots
fig, (ax1, ax2, ax3) = plt.subplots(3,1)
fig.set_size_inches(12,10)
subplot(ax1,df,'hue')
subplot(ax2,df,'saturation')
subplot(ax3,df,'value')

# save
outdir = '/home/sam/git/crater_lakes/plots/'+target
if not os.path.exists(outdir):
  os.mkdir(outdir)
os.chdir(outdir)
plt.savefig(target+'_HSV.png')