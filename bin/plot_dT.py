#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_dT.py

Plots the difference temperature (dT) between the lake and the background

"""

def plot_dT(ax, data, start, stop):
  """
  Plots delta Temperature time series
  """
  
  # set time period (x axis)
  ax.set_xlim(start, stop)
  
  # set y limit?
  #ax.set_ylim(0,0.6)
  
  # Trend line
  ax.plot(data['datetimes'],data['dT'],'k')  

  # satellite symbols
  satellite_symbols = {
                      'L4':'s',
                      'L5':'*',
                      'L7':'o',
                      'L8':'D',
                      #'AST':'^',
                      }
  for i in range(len(data['satellites'])):
    symbol = satellite_symbols[data['satellites'][i]]
    ax.plot(data['datetimes'][i],data['dT'][i],symbol+'k')

  # label axes
  ax.set_xlabel('Year')
  ax.set_ylabel(r'$\Delta$T ($^{o}$C)')