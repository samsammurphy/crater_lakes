#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

strip_json_extention.py

strips '.json' extension from all files in a directory

Created on Sat Feb  4 10:15:50 2017

@author: sam
"""

import glob
import os

path = '/home/sam/git/crater_lakes/atmcorr/v2/'

for filename in glob.iglob(path+'/**/*.json', recursive=True):
  if filename.endswith('.json'):
    os.rename(filename, filename[:-5])

