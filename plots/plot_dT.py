#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_dT.py

Plots the difference temperature (dT) between the lake and the background

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
  chart.set_ylabel('dT')
  
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
  
  dT = [d['dT'] for d in data]
  
  # Dates
  datetimes = [datetime.datetime.fromtimestamp(d['timestamp']) for d in data]
                
  # Trend line
  chart.plot(datetimes,dT,'k')  
  
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
    chart.plot(datetimes[i],dT[i],symbol+'k')



def main():
  
  target = 'Aoba'
  
  data = chronological_data(target)
  
  chart = define_plot_space()

  plot_time_series(chart,data)
   

if __name__ == '__main__':
  main()  