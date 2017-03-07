#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

pearsons_correlation_window

Created on Fri Feb 24 13:49:18 2017
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




df = load_dataFrame('Kelimutu_b')
dBT = clean_series(df,'dBT')
value = clean_series(df,'value')


dBT = np.array(dBT)
value = np.array(value)

plt.plot(dBT)
plt.show()

plt.plot(value)
plt.show()


plt.scatter(dBT,value)
corr = np.corrcoef(dBT,value)
print('Pearsons coefficient = ',corr)
