#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

plot_time_series_v6.py

"""

import pandas as pd
import matplotlib.pylab as plt


def read_excel(target,source):
  """
  Reads excel file for given target (i.e. lake) and source (i.e. satellite or
  field data)
  """
  
  # read excel file
  bpath = '/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/data/{0}/{0}'.format(target)
  fpath = '{0}_{1}.xlsx'.format(bpath,source)
  df = pd.read_excel(fpath)

  # set datetime as index
  if 'datetime' in df.keys():
    df = df.set_index(pd.DatetimeIndex(df['datetime']))
  else:
    df = df.set_index(pd.DatetimeIndex(df['date']))
  
  return df


def plot_unrest_and_eruptions(field,ax):
  """
  Plots unrest and eruptions
  
  - skips zero values for faster plotting
  - unrest = grey
  - eruption = red
  """
  
  unrest = field['unrest'][field['unrest'] == 1]
  eruption = field['eruption'][field['eruption'] == 1]
    
  for date in unrest.index:
    ax.axvline(x=date,color='#7f7f7f')
    
  for date in eruption.index:
    ax.axvline(x=date,color='#d62728')




# target lake
target = 'Kelimutu_c'

# satellite data
sat = read_excel(target,'satellite')
sat = sat.resample('3M').agg('mean').interpolate(method='time')

## field data
#field = read_excel(target,'field')
#
## plot RGB image
##RGB = list(zip(R,G,B))
##RGB_strecthed = np.array(RGB) * 1/np.max(RGB)
#
## 3 eruption subplots
#fig.tight_layout()
#for ax in [ax1,ax2,ax3]:
#  plot_unrest_and_eruptions(field,ax)


fig, (ax1, ax2, ax3) = plt.subplots(3,1, sharex = True)
fig.set_size_inches(12,10)

# hue
ax1.plot(sat['hue'])
ax1.set_ylabel('hue')

# saturation
ax2.plot(sat['saturation'])
ax2.set_ylabel('saturation')

# value
ax3.plot(sat['value'])
ax3.set_ylabel('value')









