#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

atmcorr_batch.py

Created on Sat Feb  4 12:24:19 2017
@author: sam
"""

from atmcorr_lake_time_series import run_atmcorr

# volcano_names
volcano_names = []
f = open('/home/sam/Dropbox/HIGP/Crater_Lakes/z/Volcanoes/volcano_names.txt')
for line in f:
  volcano_names.append(line.rstrip())

# check directory exist for each volcano name
for target in ['Kelimutu_a','Kelimutu_b','Kelimutu_c']:
  print(target)
  try:
    run_atmcorr(target,force=False)
  except:
    pass



