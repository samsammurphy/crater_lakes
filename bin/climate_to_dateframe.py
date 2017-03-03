#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

climate_to_dateframe.py

Reads climate files and converts to a single pandas dataframe. 

Created on Thu Mar  2 17:29:02 2017
@author: sam
"""


import glob
import pandas as pd

def read_numeric_column(lines,pos):
  """
  Reads numeric data in a column to float.  
  """  
  return [float(line[pos[0]:pos[1]]) \
          if '*' not in line[pos[0]:pos[1]] \
          else pd.np.nan for line in lines]  


def txt_to_pandas(fpath):
  """
  Reads a text file and converts to pandas dataframe
  """
  # open text file
  file = open(fpath)
  
  # read file to list 
  lines = file.readlines()
  
  # header
  lines.pop(0)
  
  # columns of itnerest
  datetime = [pd.datetime.strptime(line[13:25],'%Y%m%d%H%M') for line in lines] 
  data = {
      'wind_direction': read_numeric_column(lines,(27,29)), # degrees from magnetic north
      'wind_speed': read_numeric_column(lines,(30,33)), # miles per hour                              
      'visibility': read_numeric_column(lines,(52,56)), # miles
      'temperature ': read_numeric_column(lines,(83,87)),
      'dew_point': read_numeric_column(lines,(88,92)),
      'sea_level_pressure': read_numeric_column(lines,(93,99)),
      'station_pressure': read_numeric_column(lines,(106,112)),
      'precipitation_6hour': read_numeric_column(lines,(127,132)),
      'precipitation_24hour': read_numeric_column(lines,(133,138))
      } 
  
  # return pandas dataframe
  return pd.DataFrame(data,index=pd.DatetimeIndex(datetime))


# open climate file 
bpath = '/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/data/Kelimutu/climate/'
fpaths = sorted(glob.glob(bpath+'Met*.txt'))

# read file to df list
dfs = []
for fpath in fpaths:
  dfs.append(txt_to_pandas(fpath))

# concatenate into single dataframe
df = pd.concat(dfs)

# write to file
df.to_pickle(bpath+'all_Met_1987_2017.pkl')