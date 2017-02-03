#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atmcorr_to_CSV.py, Sam Murphy (2017-02-02)

Atmospheric correction is saved to pickle files, this module reads those files
and converts to .CSV files (i.e. to send to other people) 

"""

import csv
from load_atmcorr import chronological_data

  
target = 'Aoba'
data = chronological_data(target)

outdir = '/home/sam/git/crater_lakes/atmcorr/results/{}/'.format(target)

with open(outdir+target+'.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['satellite, fileID, timestamp,blue,green,red,dT,lake_size,cloud'])
    for d in data:      
      writer.writerow([d['satellite'],d['fileID'],d['timestamp'],\
                       d['sr']['blue'],d['sr']['green'],d['sr']['red'],d['dT'],\
                       d['lake_size'],d['cloud']])
 

