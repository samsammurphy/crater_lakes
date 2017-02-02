#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_dT.py

Plots the difference temperature (dT) between the lake and the background

"""

import pickle
import datetime
from matplotlib import pylab as plt


def load_data(target,satellites):
  """
  Loads all surface reflectance data into single dictionary
  """
  
  base_path = '/home/sam/git/crater_lakes/atmcorr/results/{}/'.format(target)
  
  data = {}
  
  for sat in satellites:
    
    fname = '{}{}_{}.p'.format(base_path,target,sat)
    sat_data = pickle.load(open(fname,"rb"))
    # datetime
    date = [datetime.datetime.fromtimestamp(d['timestamp']) for d in sat_data]
    # dT
    dT = [d['dT'] for d in sat_data]
    # add to data
    data[sat] = (date,dT)
    
  return data



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

  
  
def plot_time_series_lines(chart,data):
  """
  Plots all time series together using single trend line
  """
     
  dates = []
  values = []
  
  for sat in ['L4','L5','L7','L8','AST']:
    
    if data[sat][0]:
      dates += data[sat][0]
      values += data[sat][1]
        
  #chronologic sort
  chronological = sorted(zip(dates,values), key=lambda x: x[0])
  dates = [x[0] for x in chronological]
  values = [x[1] for x in chronological]
  
  chart.plot(dates,values,'k')  
  

  
def plot_satellite_points(chart,data):
  """
  Overplots satellite data points
  """
    
  satellite_symbol = {
                      'L4':'s',
                      'L5':'*',
                      'L7':'o',
                      'L8':'D',
                      'AST':'^',
                      }
  
  for sat in data.keys():
    symbol = satellite_symbol[sat]
     
    date = data[sat][0]
    value = data[sat][1]
    
    chart.plot(date,value,'k'+symbol)
   


def main():
  
  target = 'Aoba'
  
  satellites = ['L4','L5','L7','L8','AST']
  
  data = load_data(target,satellites)
  
  chart = define_plot_space()
    
  # plot trend line (all satellites)
  plot_time_series_lines(chart,data)
  
  # plot unique symbols for each satellite
  plot_satellite_points(chart,data)
   

if __name__ == '__main__':
  main()  