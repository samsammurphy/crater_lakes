#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

switch_sat_target.py

patch to switch the position of satellite and target names within
the GEE geojson file.

Created on Wed Feb 22 10:21:38 2017

@author: sam
"""


import glob
import os
import re

path = '/home/sam/git/crater_lakes/atmcorr/LakesData'

for fpath in glob.iglob(path+'/**/*.geojson', recursive=True):
  fname = os.path.basename(fpath)
  
  for satname in ['AST','L4','L5','L7','L8']:
    m = re.match(satname,fname)
    if m:
      if m.start() == 0:
        remove_satname = fname[m.end()+1:]
        split = remove_satname.split('.')
        new_fname = '{0[0]}_{1}.{0[1]}'.format(split,satname)
        os.rename(fpath, os.path.dirname(fpath)+'/'+new_fname)