#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

atmcorr_batch.py

Created on Sat Feb  4 12:24:19 2017
@author: sam
"""

from atmcorr_lake_time_series import run_atmcorr

targets = ['Poas','Kusatsu-Shirane','Copahue','Aso']

for target in targets:
  try:
    run_atmcorr(target)
  except:
    pass





