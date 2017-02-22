#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

atmcorr_to_EXCEL.py

Created on Thu Feb 16 17:00:24 2017
@author: sam
"""

import pickle
import itertools
import datetime
import colorsys
import pandas as pd
import numpy as np


def load_sat(target,sat): 
  base_path = '/home/sam/git/crater_lakes/atmcorr/results/{}/'.format(target)
  fname = '{}{}_{}.p'.format(base_path,target,sat)
  data = pickle.load(open(fname,"rb"))
  return data
  
def timestamp_sort(dictionary):
  return dictionary['timestamp']
  
def get_HSV(data):
  r = [x['sr']['red'] for x in data]
  g = [x['sr']['green'] for x in data]
  b = [x['sr']['blue'] for x in data]
  
  rgb = list(zip(r,g,b))
  
  hsv = [colorsys.rgb_to_hsv(x[0],x[1],x[2]) \
         if np.min(x) >= 0 and np.max(x[1]) <= 1 \
         else np.repeat(np.NaN,3) for x in rgb]
  
  return hsv
  

target = 'Ruapehu'

# Load all Landsat data into single chronological list
L4 = load_sat(target,'L4')  
L5 = load_sat(target,'L5')  
L7 = load_sat(target,'L7')  
L8 = load_sat(target,'L8')  
data = list(itertools.chain(L4,L5,L7,L8))#,AST
data = sorted(data,key=timestamp_sort)

# Calculate HSV color space
hsv = get_HSV(data)

df = pd.DataFrame({
    'datetime':[datetime.datetime.fromtimestamp(x['timestamp']) for x in data],
    'timestamp':[x['timestamp'] for x in data],
    'satellite':[x['satellite'] for x in data],
    'fileID':[x['fileID'] for x in data],
    'lake_size':[x['lake_size'] for x in data],
    'cloud':[x['cloud'] for x in data],
    'AOT':[x['params']['AOT'] for x in data],
    'red':[x['sr']['red'] for x in data],
    'green':[x['sr']['green'] for x in data],      
    'blue':[x['sr']['blue'] for x in data],
    'hue':[x[0] for x in hsv],
    'saturation':[x[1] for x in hsv],
    'value':[x[2] for x in hsv],
    'dBT':[x['T']['dBT'] for x in data],
    'dTsurface':[x['T']['dTsurface'] for x in data],
    'BT_lake':[x['T']['BT_lake'] for x in data],
    'BT_bkgd':[x['T']['BT_bkgd'] for x in data]
    })


writer = pd.ExcelWriter('/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/'
                        'data/{0}/{0}_satellite.xlsx'.format(target))
df.to_excel(writer,columns=\
['datetime','timestamp','satellite','fileID','lake_size','cloud','AOT',\
'red','green','blue','hue','saturation','value',\
'dBT','dTsurface','BT_lake','BT_bkgd'])
writer.save()