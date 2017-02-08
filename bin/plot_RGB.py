#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_RGB.py

Plots visible surface reflectance for all satellites onto a chart (i.e. 'axes')

"""

import datetime

def plot_RGB(ax, data, start, stop):
  """
  Plots RGB time series
  """
  
  # set time period (x axis)
  ax.set_xlim(start, stop)
  
  # set y limit?
  #ax.set_ylim(0,0.6)
  
  # extract RGB
  blue = [d['sr']['blue'] for d in data]
  green = [d['sr']['green'] for d in data]
  red = [d['sr']['red'] for d in data]
  
  # dates
  datetimes = [datetime.datetime.fromtimestamp(d['timestamp']) for d in data]
                
  # Trend line
  ax.plot(datetimes,red,'r')  
  ax.plot(datetimes,green,'g')
  ax.plot(datetimes,blue,'b')    
  
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
    ax.plot(datetimes[i],red[i],symbol+'r')
    ax.plot(datetimes[i],green[i],symbol+'g')
    ax.plot(datetimes[i],blue[i],symbol+'b')
    
