#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

plot_HSV.py

Created on Tue Feb  7 14:36:43 2017
@author: sam
"""

import datetime
import colorsys

def plot_HSV(ax, data, start, stop):
  """
  Plots HSV time series
  """
  
  # set time period (x axis)
  ax.set_xlim(start, stop)
  
  # set y limit?
  #ax.set_ylim(0,0.6)
  
  # extract RGB
  R = [d['sr']['red'] for d in data]
  G = [d['sr']['green'] for d in data]
  B = [d['sr']['blue'] for d in data]
  
  # convert to HSV
  hsv = [colorsys.rgb_to_hsv(r,g,b) for r,g,b in list(zip(R,G,B))] 
  hue = [x[0] for x in hsv]
  saturation = [x[1] for x in hsv]
  value = [x[2] for x in hsv]
  
  # dates
  datetimes = [datetime.datetime.fromtimestamp(d['timestamp']) for d in data]
                
  # Trend line
  #ax.plot(datetimes,hue,'y')  
  ax.plot(datetimes,saturation,'m')
  ax.plot(datetimes,value,'c')    
  
  # satellite symbols
  satellites = [d['satellite'] for d in data]
  satellite_symbols = {
                      'L4':'s',
                      'L5':'*',
                      'L7':'o',
                      'L8':'D',
                      #'AST':'^',
                      }
  for i in range(len(satellites)):
    symbol = satellite_symbols[satellites[i]]
    #ax.plot(datetimes[i],hue[i],symbol+'y')
    ax.plot(datetimes[i],saturation[i],symbol+'m')
    ax.plot(datetimes[i],value[i],symbol+'c')
    
