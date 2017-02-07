#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_size.py

Plots size of lake and amount of cloud cover
"""

from load_atmcorr import chronological_data
import datetime
from matplotlib import pylab as plt


def define_plot_space():
  
  # figure instance
  fig = plt.figure()
  chart = fig.add_subplot(1,1,1) # a.k.a. 'axes'
  
  # label axes
  chart.set_xlabel('Date')
  chart.set_ylabel('Size')
  
  # x limits (time period)
  start = datetime.datetime(2000,1,1)
  stop  = datetime.datetime(2016,1,1)
  chart.set_xlim(start, stop)
  
  # y limits (reflectance)
  #chart.set_ylim(0,0.6)
  
  return chart
 
def plot_time_series(chart,data):
  """
  Plots time series
  """
  
  size = [d['lake_size'] for d in data]
  cloud = [d['cloud'] for d in data]
  datetimes = [datetime.datetime.fromtimestamp(d['timestamp']) for d in data]
                
  # Trend line
  chart.plot(datetimes,size,'c')  
  chart.plot(datetimes,cloud,'y')
   
  
  # Satellite symbols
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
    chart.plot(datetimes[i],size[i],symbol+'c')
    chart.plot(datetimes[i],cloud[i],symbol+'y')


def main():
  
  target = 'Aoba'
  
  data = chronological_data(target)
  
  chart = define_plot_space()

  plot_time_series(chart,data)
  
if __name__ == '__main__':
  main()  