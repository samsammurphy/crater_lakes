#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

plot_greyness_and_value.py

Created on Tue Feb  7 15:29:50 2017
@author: sam
"""

import colorsys

def plot_greyness_and_value(ax, data, start, stop):
  """
  Plots HSV time series
  """
  
  # set time period (x axis)
  ax.set_xlim(start, stop)
  
  # set y limit
  ax.set_ylim(0,1)
  
  # extract RGB
  rgb = list(zip(data['r'],data['g'],data['b']))

  # convert to greyness and value
  hsv = [colorsys.rgb_to_hsv(r,g,b) for r,g,b in rgb] 
  greyness = [1-x[1] for x in hsv]
  value = [x[2] for x in hsv]
                  
  # trend lines
  ax.plot(data['datetimes'],greyness,'gray')
  ax.plot(data['datetimes'],value,'m')    
  
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

    ax.plot(data['datetimes'][i],greyness[i],symbol,color='gray')
    ax.plot(data['datetimes'][i],value[i],symbol+'m')

  # label axes
  ax.set_ylabel('grayness or value')