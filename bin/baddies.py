#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

baddies.py

- a bad image files manager

1) manual selection
2) cloud filtered

nb. removed after atmcorr but before excel (plots use excel)
"""

import os
import glob
import datetime


def bad_fileIDs(target):
  """
  manually define bad fileIDs
  """
  
  baddies = {
      
      'Kelimutu_a':['LT51120662008282ASA00',\
                    'LT51120661997331ASA00',\
                    'LT51120661996345DKI00'],
      
      'Kelimutu_c': ['LT51120662000004ASA00'],
                  
      'Yugama':['LT51080352001058BJC00',\
                'LT51080352001138BJC01',\
                'LT51080352002061BJC01',\
                'LT51080352002077BJC00',\
                'LT51080352002093BJC00']
      
      }
  
  if target in baddies.keys():
    return baddies[target]
  else :
    return []

def cloud_filtered(data,target):
  """
  automatically assign bad fileIDs to images that do not pass cloud filter
  """
  
  #1) cloud_filtered dates
  cloud_filtered_dir = '/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/Kelimutu/RGBs/cloud_filtered_(manually)/'
  fpaths = glob.glob(cloud_filtered_dir+'*.tif')
  good_dates = [os.path.basename(f).split('.')[0] for f in fpaths]
  
  #2) original fileIDs and dates
  all_fileIDs = [x['fileID'] for x in data]
  all_dates = [datetime.datetime.utcfromtimestamp(x['timestamp']) for x in data]

  #3) compare dates, append baddies
  
  baddies = []
  
  for i, date in enumerate(all_dates):
    if date.strftime('%Y_%m_%d_%H%M') not in good_dates:
      baddies.append(all_fileIDs[i])
  
  return baddies
  

def naughty_list(data,target):
  """
  Compile the naughty list from manually selected fileIDs and cloud filter
  assigned fileIDs
  """
  
  baddies = bad_fileIDs(target)
  baddies += cloud_filtered(data,target)
  
  return baddies
      

      

  
  
  
  
  