#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

plot_normalized_temperatures.py

Created on Tue Feb  7 18:44:17 2017
@author: sam
"""


import os
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import datetime


target = 'Yugama'

# load data
os.chdir('/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/data/'+target)
df = pd.read_excel(target+'.xlsx')

# target variables
dBT = np.array(df['dBT'])
fieldT = np.array(df['T'])
timestamps = df['timestamp']

# ok satellite days (i.e. within 3 std from mean)
ok = np.where(abs(dBT) <= np.mean(dBT)+3*np.std(dBT))[0]
dBT = dBT[ok]
fieldT = fieldT[ok]
timestamps = timestamps[ok]
       
# normalize
def normalize(timestamp,variable):
  
  ok = ~pd.isnull(variable)
  t = timestamp[ok]
  v = variable[ok]
  
  norm = (v-np.mean(v))/np.std(v)
  
  return t, norm
  
dBT_norm = normalize(timestamps,dBT)
fieldT_norm = normalize(timestamps,fieldT)

# plot
datetimes = [datetime.datetime.fromtimestamp(t) for t in timestamps]
plt.plot(dBT_norm[0],dBT_norm[1],'ko')
plt.plot(fieldT_norm[0],fieldT_norm[1],'rD')
plt.xlabel('year')
plt.ylabel('normalized temperatures')
plt.show()


def scatter(var1,var2):
  ok = ~pd.isnull(var1) * ~pd.isnull(var2)
  var1 = var1[ok]
  var2 = var2[ok]
  
  # normalize
  n1 = (var1-np.mean(var1))/np.std(var1)
  n2 = (var2-np.mean(var2))/np.std(var2)
  
  plt.scatter(var1,var2)
  plt.show()
  
  plt.scatter(n1,n2)
  plt.show()

scatter(dBT,fieldT)
