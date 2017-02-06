#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

strip_Ldata_prefix.py

strips off th Ldata prefix (which was used to get a unique GEE folder name)


Created on Sat Feb  4 20:10:52 2017
@author: sam
"""

import os

directory = '/home/sam/git/crater_lakes/atmcorr/lake_data'
subpaths = [x[0] for x in os.walk(directory)][1:]

for subpath in subpaths:
  subdir = os.path.basename(subpath)
  if subdir.startswith('Ldata_'):
    newpath = os.path.dirname(subpath)+'/'+subdir[6:]
    os.rename(subpath,newpath)


#