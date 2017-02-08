#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_dT.py

Plots the difference temperature (dT) between the lake and the background

"""

import datetime

 
def plot_dT(ax, data, start, stop):
  """
  Plots delta Temperature time series
  """
  
  # set time period (x axis)
  ax.set_xlim(start, stop)
  
  # set y limit?
  #ax.set_ylim(0,0.6)
  
  # extract dT
  dT = [d['T']['dBT'] for d in data]
  
  # dates
  datetimes = [datetime.datetime.fromtimestamp(d['timestamp']) for d in data]
                
  # Trend line
  ax.plot(datetimes,dT,'k')  

  # satellite symbols
  satellites = [d['satellite'] for d in data]
  satellite_symbols = {
                      'L4':'s',
                      'L5':'*',
                      'L7':'o',
                      'L8':'D',
                      'AST':'^',
                      }
  for i in range(len(satellites)):
    symbol = satellite_symbols[satellites[i]]
    ax.plot(datetimes[i],dT[i],symbol+'k')
