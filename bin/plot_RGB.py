#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_RGB.py

Plots visible surface reflectance for all satellites onto a chart (i.e. 'axes')

"""

def plot_RGB(ax, data, start, stop):
  """
  Plots RGB time series
  """
  
  # set time period (x axis)
  ax.set_xlim(start, stop)
  
  # set y limit
  ax.set_ylim(0,1)
                 
  # trend line
  ax.plot(data['datetimes'],data['r'],'r')  
  ax.plot(data['datetimes'],data['g'],'g')
  ax.plot(data['datetimes'],data['b'],'b')    
  
  # satellite symbols
  satellites = data['satellites']
  satellite_symbols = {
                      'L4':'s',
                      'L5':'*',
                      'L7':'o',
                      'L8':'D',
                      #'AST':'^',
                      }
  for i in range(len(satellites)):
    symbol = satellite_symbols[satellites[i]]
    ax.plot(data['datetimes'][i],data['r'][i],symbol+'r')
    ax.plot(data['datetimes'][i],data['g'][i],symbol+'g')
    ax.plot(data['datetimes'][i],data['b'][i],symbol+'b')
    
  # y label
  ax.set_ylabel('reflectance')