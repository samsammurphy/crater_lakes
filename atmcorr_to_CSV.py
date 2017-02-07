#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atmcorr_to_CSV.py, Sam Murphy (2017-02-02)

Atmospheric correction is saved to pickle files, this module reads those files
and converts to .CSV files (i.e. to send to other people) 

"""

from load_atmcorr import chronological_data
import csv
import colorsys
import datetime

  
target = 'Poas'
data = chronological_data(target)

outdir = '/home/sam/git/crater_lakes/atmcorr/results/{}/'.format(target)

with open(outdir+target+'.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['year, month, day, hour, minute,timestamp,satellite, fileID,'\
    'red,green,blue,H,S,V,BT_lake,BT_bkgd,dBT,dT_surface,lake_size'])
    for d in data:      
      # read visible
      r = d['sr']['red']
      g = d['sr']['green']
      b = d['sr']['blue']
      # read thermal
      BTlake = d['T']['BT_lake']
      BTbkgd = d['T']['BT_bkgd']
      dBT = d['T']['dBT']
      dTsurface = d['T']['dTsurface']
      
      # datetime
      date = datetime.datetime.fromtimestamp(d['timestamp'])
      if b:      
        H, S, V = colorsys.rgb_to_hsv(r,g,b)    
        writer.writerow([date.year,date.month,date.day,date.hour,date.minute,\
                         d['timestamp'],d['satellite'],d['fileID'],\
                         r,g,b,H,S,V,\
                         BTlake,BTbkgd,dBT,dTsurface,\
                         d['lake_size']])
 

#      saturation2D = abs(r-g)
#      value2D = max(r,g)
