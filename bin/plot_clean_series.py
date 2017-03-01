#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

plot_clean_series.py

clean
1) resampled to same frequency
2) remove null values (linear interpolation)


NB. (DEPRECATED) Used to be able to do this with Series.rolling() too, i.e.
using the freq keyword. You should avoid. Just stick with Series.resampled(), 
it is much clearer and therefore easier to follow intent.
"""

import pandas as pd

def read_time_series(target,varname):
  
  # load excel file from lake name (i.e. 'a','b' or 'c') 
  base_path = '/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/data/'
  file_path = base_path+'{0}/{0}_satellite.xlsx'.format(target)
  df = pd.read_excel(file_path)
  
  # extract time series
  values = pd.np.array(df[varname])
  dates = pd.DatetimeIndex(df['datetime'])
  time_series = pd.Series(values,dates)
  
  return time_series
  

def resample_time_series(s):
  """
  1) Resample and interpolate
  """
    
  # resample time series over 8 days
  r = s.resample('8D').agg('mean')
  
  # remove null values
  return r.interpolate(method='time')

def main():
  # original series
  s = read_time_series('Kelimutu_b','value')
  
  # clean series
  resampled = resample_time_series(s)
  
  # plot
  s.plot(style='co-')
  resampled.plot(style='r.')


if __name__ == '__main__':
  main()



























