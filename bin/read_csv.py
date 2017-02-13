#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
read_csv.py

Created on Fri Feb 10 08:48:07 2017
@author: sam
"""

import os
import pandas as pd
import numpy as np
import datetime

def read_csv(target):
  
  try:
    os.chdir('/home/sam/git/crater_lakes/atmcorr/results/'+target)
    
    df = pd.read_csv(target+'.csv')
    
    return {
      'r':np.clip(df.red.values,0,1),
      'g':np.clip(df.green.values,0,1),
      'b':np.clip(df.blue.values,0,1),
      'dT':df.dBT.values,
      'timestamps':df.timestamp.values,
      'datetimes':[datetime.datetime.fromtimestamp(t) for t in df.timestamp.values],    
      'satellites':df.satellite.values
      }
  except:
    print('File IO error for :'+target)