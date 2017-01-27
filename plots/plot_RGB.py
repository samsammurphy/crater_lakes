#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_RGB.py

Plots visible surface reflectance for all satellites onto a chart (i.e. 'axes')

"""

import pickle
import datetime
from matplotlib import pylab as plt



def read_sr_data(sat_data,name):
  """
  Reads surface reflectance for given satellite 
  """
  
  date = [datetime.datetime.fromtimestamp(d['timestamp']) for d in sat_data if name in d['sr']]
  SR = [d['sr'][name] for d in sat_data if name in d['sr']]
  
  return (date,SR)
  


def load_data(target,satellites):
  """
  Loads all surface reflectance data into single dictionary
  """
  
  base_path = '/home/sam/git/crater_lakes/atmcorr/results/{}/'.format(target)
  
  data = {}
  
  for sat in satellites:
    fname = '{}{}_{}.p'.format(base_path,target,sat)
    sat_data = pickle.load(open(fname,"rb"))
    data[sat] = {
        'blue':read_sr_data(sat_data,'blue'),
        'green':read_sr_data(sat_data,'green'),
        'red':read_sr_data(sat_data,'red')   
        }
    
  return data



def define_plot_space():
  
  # figure instance
  fig = plt.figure()
  chart = fig.add_subplot(1,1,1) # a.k.a. 'axes'
  
  # x limits (time period)
  start = datetime.datetime(2000,1,1)
  stop  = datetime.datetime(2016,1,1)
  chart.set_xlim(start, stop)
  
  # y limits (reflectance)
  chart.set_ylim(0,0.6)
  
  return chart



def waveband_colour(waveband):
  """
  Assign unqiue color to each waveband
  """  
  
  assign_color = {
                  'blue':'b',
                  'green':'g',
                  'red':'r'
                  }
                  
  return assign_color[waveband]

  
  
def plot_time_series_lines(chart,data):
  """
  Plots all time series together using single trend line
  """
  
  for waveband in ['blue','green','red']:
    
    dates = []
    values = []
    
    for sat in ['L4','L5','L7','L8','AST']:
      
      if data[sat][waveband][0]:
        dates += data[sat][waveband][0]
        values += data[sat][waveband][1]
         
    #chronologic sort
    chronological = sorted(zip(dates,values), key=lambda x: x[0])
    dates = [x[0] for x in chronological]
    values = [x[1] for x in chronological]
    
    colour = waveband_colour(waveband)

    chart.plot(dates,values,colour)  
  

  
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
    
    for waveband in data[sat].keys():
      
      date = data[sat][waveband][0]
      value = data[sat][waveband][1]
      colour = waveband_colour(waveband)
      
      chart.plot(date,value,colour+symbol)
   


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