#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_Kelimutu_compare.py

Created on Fri Feb 24 12:42:45 2017
@author: sam
"""



import pandas as pd

def clean_series(lake,varname):
  
  # load excel file from lake name (i.e. 'a','b' or 'c') 
  base_path = '/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/data/'
  file_path = base_path+'Kelimutu_{0}/Kelimutu_{0}_satellite.xlsx'.format(lake)
  df = pd.read_excel(file_path)
  
  # extract time series
  values = pd.np.array(df[varname])
  dates = pd.DatetimeIndex(df['datetime'])
  s = pd.Series(values,dates)
  
  # resample time series over 8 days (use mean value)
  r = s.resample('8D').agg('mean')
  
  # interpolate time series (i.e. removes null values)
  interpolated = r.interpolate(method='time')
  
  return interpolated

# variable of interest
varname = 'value'

# extract clean time series
sa = clean_series('a',varname)
sb = clean_series('b',varname)
sc = clean_series('c',varname)

sa.plot(style='r')
sb.plot(style='g')
sc.plot(style='b')


  