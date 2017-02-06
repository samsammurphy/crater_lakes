#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

check_downloads.py

checks to see if each of the satellite missions were downloaded

Created on Sat Feb  4 20:27:40 2017
@author: sam
"""


import os
import glob

directory = '/home/sam/git/crater_lakes/atmcorr/lake_data'
subpaths = sorted([x[0] for x in os.walk(directory)][1:])
subdirs = sorted([os.path.basename(sub) for sub in subpaths])

# check that directories contain files for each satellite mission
for subpath in subpaths:
  
  files = glob.glob(subpath+'/*.geojson')
  
  if files:
    print(subpath)
    satnames = [os.path.basename(f)[0:3] for f in files]
    if not 'AST' in satnames: print('ASTER missing')
    if not 'L4_' in satnames: print('L4 missing')
    if not 'L5_' in satnames: print('L5 missing')
    if not 'L7_' in satnames: print('L7 missing')
    if not 'L8_' in satnames: print('L8 missing')
  else:
    print('no files found in: '+subpath)
    
# volcano_names
volcano_names = []
f = open('/home/sam/Dropbox/HIGP/Crater_Lakes/z/Volcanoes/volcano_names.txt')
for line in f:
  volcano_names.append(line.rstrip())

# check directory exist for each volcano name
for name in volcano_names:
  if name not in subdirs:
    print('missing directory for: '+name)