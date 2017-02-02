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


outdir = '/home/sam/git/crater_lakes/atmcorr/results/'+target

with open('test.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['fileID, timestamp,red,green,blue,dT,size,cloud'])
    for d in data:      
      writer.writerow([d['fileID'],d['timestamp'],d['red'],d['green'],\
                       d['blue'],d['dT'],d['size'],d['cloud']])
 

