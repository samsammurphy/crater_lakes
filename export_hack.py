#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

export_hack.py

Created on Sat Feb  4 09:31:39 2017

@author: sam
"""

from export_ASTER_time_series import ASTER_export
from export_LANDSAT_time_series import LANDSAT_export

# volcano names
#fname = '/home/sam/Dropbox/HIGP/Crater_Lakes/z/Volcanoes/volcano_names.txt'
fname = '/home/sam/Desktop/volcanoes_to_get.txt'
vfile = open(fname, "r")
for i, line in enumerate(vfile):
  volcano_name = line.strip('\n')
  if i <= 0:
    print(volcano_name)
    ASTER_export(volcano_name)
  #LANDSAT_export(volcano_name)