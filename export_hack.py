#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

export_hack.py

Created on Sat Feb  4 09:31:39 2017

@author: sam
"""

import sys
sys.path.append('/home/sam/git/crater_lakes/bin/')

from export_ASTER_time_series import ASTER_export
from export_LANDSAT_time_series import LANDSAT_export

# all targets
f = open('/home/sam/Dropbox/HIGP/Crater_Lakes/z/Volcanoes/volcano_names.txt')
for line in f:
  try:
    target = line.rstrip()
    print(target)
    ASTER_export(target)
    LANDSAT_export(target)
  except:
    print('???',line)
    pass
