#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_RGB.py

Plots visible surface reflectance for all satellites onto a chart (i.e. 'axes')

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
  chart.set_ylabel('Reflectance')
  
  # x limits (time period)
  start = datetime.datetime(2000,1,1)
  stop  = datetime.datetime(2016,1,1)
  chart.set_xlim(start, stop)
  
  # y limits (reflectance)
  chart.set_ylim(0,0.6)
  
  return chart
 
def plot_time_series(chart,data):
  """
  Plots RGB time series
  """
  
  # Color
  blue = [d['sr']['blue'] for d in data]
  green = [d['sr']['green'] for d in data]
  red = [d['sr']['red'] for d in data]
  
  # Dates
  datetimes = [datetime.datetime.fromtimestamp(d['timestamp']) for d in data]
                
  # Trend line
  chart.plot(datetimes,red,'r')  
  chart.plot(datetimes,green,'g')
  chart.plot(datetimes,blue,'b')    
  
  # Satellite symbols
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
    chart.plot(datetimes[i],red[i],symbol+'r')
    chart.plot(datetimes[i],green[i],symbol+'g')
    if blue[i]:
      chart.plot(datetimes[i],blue[i],symbol+'b')
    

def main():
  
  target = 'Poas'
  
  data = chronological_data(target)
  
  chart = define_plot_space()

  plot_time_series(chart,data)
  
if __name__ == '__main__':
  main()  