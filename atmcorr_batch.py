#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

atmcorr_batch.py

Created on Sat Feb  4 12:24:19 2017
@author: sam
"""

# terminal friendly
import sys
sys.path.append("/home/sam/git/crater_lakes/bin")
from atmospheric_correction import run_atmcorr

# all targets
f = open('/home/sam/Dropbox/HIGP/Crater_Lakes/z/Volcanoes/volcano_names.txt')
for line in f: #for target in ['Ruapehu']:#['Poas','Yugama','Kelimutu_a','Kelimutu_b','Kelimutu_c']:
  target = line.rstrip()
  print(target)
  try:
    run_atmcorr(target,force=True)
  except:
    pass



