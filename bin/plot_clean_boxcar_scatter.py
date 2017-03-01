#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_clean_convolved_scatter.py

Created on Fri Feb 24 14:21:21 2017
@author: sam
"""


import pandas as pd
import numpy as np
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



var1 = 'value'
var2 = 'saturation'
target = 'Kelimutu_b'

# load clean series
df = load_dataFrame(target)
s1 = clean_series(df,var1)
s2 = clean_series(df,var2)

# boxcar
window_size = 100
b1 = s1.rolling(window=window_size,center=True).mean()
b2 = s2.rolling(window=window_size,center=True).mean()

# plot time series
plt.plot(s1)
plt.plot(b1)
plt.ylabel(var1)
plt.show()
plt.plot(s2)
plt.plot(b2)
plt.ylabel(var2)
plt.show()

# plot scatter
plt.scatter(np.array(s1),np.array(s2))
plt.scatter(np.array(b1),np.array(b2))
plt.xlabel(var1)
plt.ylabel(var2)

print('Pearsons coefficient full = ',s1.corr(s2))
print('Pearsons coefficient boxcar = ',b1.corr(b2))
