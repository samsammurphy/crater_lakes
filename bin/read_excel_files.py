#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

read_excel_files.py

a bit of sugar to help read the excel files nicely


Created on Mon Feb 27 15:57:27 2017
@author: sam
"""

import pandas as pd

class read_field_data():
  """
  A field data object containing a pandas dataframe
  """
  
  def __init__(self,target):
    
    base_path = '/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/data/'
    file_path = base_path+'{0}/{0}_field.xlsx'.format(target)
    df = pd.read_excel(file_path)
    
    # set date column as DatetimeIndex
    df = df.set_index(pd.DatetimeIndex(df['date']))
    
    self.target = target
    self.df = df
    

class read_satellite_data():
  """
  A satellite data object containing a pandas dataframe and a method to
  resample and interpolate time series (i.e. constant frequenct, no nulls)
  """
  
  def __init__(self,target):
    "initialize target name load excel file"
    
    base_path = '/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/data/'
    file_path = base_path+'{0}/{0}_satellite.xlsx'.format(target)
    df = pd.read_excel(file_path)
    
    # set datetime column as DatetimeIndex
    df = df.set_index(pd.DatetimeIndex(df['datetime']))
    
    self.target = target
    self.df = df

  def resampledSeries(self,frequency,seriesName, inverted=False):
    "resamples a time series to a set frequency and fill null values"
    
    # pandas time series
    t = pd.DatetimeIndex(self.df['datetime'])# time (t) 
    y = pd.np.array(self.df[seriesName])     # value (y)   
    if inverted:                             # greyness?
      y = 1-y
      
    s = pd.Series(y,t)
    
    # resample to fixed frequency
    r = s.resample(frequency).agg('mean')
    
    # interpolate (i.e. remove null values)
    i = r.interpolate(method='time')
        
    return i
  
  def resampled(self, frequency):
    "resamples a collection of numeric time series"
    
    df = pd.DataFrame({
        'hue':self.resampledSeries(frequency,'hue'),
        'saturation':self.resampledSeries(frequency,'saturation'),
        'greyness':self.resampledSeries(frequency,'saturation',inverted=True),
        'value':self.resampledSeries(frequency,'value'),
        'dBT':self.resampledSeries(frequency,'dBT')
      })
  
    return df