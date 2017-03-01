#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_clean_boxcar_series.py

Created on Fri Feb 24 14:21:21 2017
@author: sam
"""


import pandas as pd
import matplotlib.pylab as plt

def load_dataFrame(target):
  base_path = '/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/data/'
  file_path = base_path+'{0}/{0}_satellite.xlsx'.format(target)
  df = pd.read_excel(file_path)
  
  return df

def clean_series(df,varname):
   
  # extract time series
  values = pd.np.array(df[varname])
  dates = pd.DatetimeIndex(df['datetime'])
  s = pd.Series(values,dates)
  
  # resample time series over 8 days (use mean value)
  r = s.resample('8D').agg('mean')
  
  # interpolate time series (i.e. removes null values)
  interpolated = r.interpolate(method='time')
  
  return interpolated



var = 'saturation'
target = 'Kelimutu_b'

# load clean series
df = load_dataFrame(target)
s = clean_series(df,var)

# plot original data
plt.plot(s)
plt.ylabel(var)

# plot rolling window
boxcar = s.rolling(window=10,center=True).mean()
plt.plot(boxcar)

