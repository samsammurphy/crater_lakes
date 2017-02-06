#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

atmcorr_batch.py

Created on Sat Feb  4 12:24:19 2017
@author: sam
"""

from atmcorr_lake_time_series import run_atmcorr

#TODO run through all volcano names, look for satellite files in lake data, if atmcorr for that satellite doesnt already exist then run_atmcorr for that satellite onlu


targets = ['Poas','Kusatsu-Shirane','Copahue','Aso']

for target in targets:
  try:
    run_atmcorr(target)
  except:
    pass





