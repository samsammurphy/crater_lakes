#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

plot_time_series_v6.py

Created on Mon Feb  6 20:53:54 2017
@author: sam
"""
import os
import sys
import pandas as pd
import numpy as np
import datetime
import time
import matplotlib.pylab as plt
import matplotlib.dates as mdates
import colorsys
import math


def null_handler(df):
  """
  Handles missing data values
  """
  
  # define ok as hue = True
  ok = np.array([~pd.isnull(df['hue'])])[0]
  
  # filter arrays
  r = df['red'][ok]
  g = df['green'][ok]
  b = df['blue'][ok]
  h = df['hue'][ok]
  s = df['saturation'][ok]
  v = df['value'][ok]
  dBT = df['dBT'][ok]
  dt = df['datetime'][ok] 
  t = [datetime.datetime.timestamp(x) for x in dt]
  
  return (r,g,b,h,s,v,dBT,dt,t)
  

def interpolate_triplet(r,g,b,timestamps, start, stop, maxv = None):
  """
  Interpolates color triplet over daily frequency
  """
  numdays = (stop-start).days
  hires_dates = [start + datetime.timedelta(days=x) for x in range(0,numdays)]
  hires_time = [time.mktime(date.timetuple()) for date in hires_dates]

  # interpolate r,g,b
  R = np.interp(hires_time, timestamps, r)
  G = np.interp(hires_time, timestamps, g)
  B = np.interp(hires_time, timestamps, b)

  return (R, G, B)

def pure_hue(R, G, B):
  true_hsv = [colorsys.rgb_to_hsv(x[0],x[1],x[2]) for x in list(zip(R,G,B))]
  pure_hue = [colorsys.hsv_to_rgb(x[0],1,1) for x in true_hsv]
  return pure_hue

def rgb_stretch(R,G,B, target):
  """
  Linear stretch of R, G, B and zip together, 
  """
  
  top = {'Kelimutu_a':0.2,'Kelimutu_b':0.5,'Kelimutu_c':0.2}[target]

  R = np.clip(R/top,0,1)
  G = np.clip(G/top,0,1)
  B = np.clip(B/top,0,1)
  return list(zip(R,G,B))

def interpolate_series(t,y,start,stop):
  """
  Interpolates a time series over daily frequency
  """
 
  # daily timestamsp
  numdays = (stop-start).days
  D = [start + datetime.timedelta(days=x) for x in range(0,numdays)]
  T = [time.mktime(date.timetuple()) for date in D]
  
  # interpolated variable
  Y = np.interp(T, t, y)
  
  return (D, Y)

def boxcar_average(D,Y,N):
  """
  Box car average from interpolated values
  """
  boxY = np.convolve(Y, np.ones((N,))/N, mode='valid')
  edge = (len(Y)-len(boxY))/2 
  boxD = D[math.floor(edge):-math.ceil(edge)]
  
  return (boxD, boxY)

def define_axes(fig):

  plot_height = 0.22
  bar = 0.15
  minibar = 0.03
  gap = 0.05
  mini_gap = 0.03
  axRGB = fig.add_axes([0.1,gap+3*plot_height+3*mini_gap+minibar,0.87,bar])
  axH = fig.add_axes([0.1,gap+3*plot_height+2.5*mini_gap,0.87,minibar])
  axS = fig.add_axes([0.1,gap+2*plot_height+2*mini_gap,0.87,plot_height])
  axV = fig.add_axes([0.1,gap+plot_height+mini_gap,0.87,plot_height])
  axT = fig.add_axes([0.1,gap,0.87,plot_height])
  
  return (axRGB, axH, axS, axV, axT)

def plot_colorbar(ax,image,ylabel=False):
  ax.imshow(image, interpolation='nearest', aspect='auto')
  ax.set_xticks([])
  ax.set_yticks([])
  ax.set_ylabel(ylabel)

def plot_timeseries(ax,t,dt,y,start,stop,ylabel=False,color='#1f77b4'):
  
  # original time series
  ax.plot(dt,y,color=color)
  ax.set_ylabel(ylabel)
  ax.set_xlim(start,stop)
  
  # boxcar
  D, Y = interpolate_series(t,y,start,stop)
  boxD, boxY = boxcar_average(D,Y,180)
  ax.plot(boxD,boxY,'r-')
  
  # make the dates exact
  ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')

def plotting_manager(target):
  """
  Loads data, creates figures, inserts subplots
  """
  
  # read data
  base_dir = '/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/Kelimutu'
  df = pd.read_excel('{0}/{1}/{1}_satellite.xlsx'.format(base_dir,target))
  r,g,b,h,s,v,dBT,dt,t = null_handler(df)

  # define time period
  start = datetime.datetime(1987,1,1)
  stop  = datetime.datetime(2017,1,1) 

  # interpolate r, g, b
  R, G, B = interpolate_triplet(r,g,b,t,start,stop)

  # Idealized Hue (saturation = 1, value = 1)
  Hue = pure_hue(R,G,B)

  # define figure
  fig = plt.figure(figsize=(8,12))
  axRGB, axH, axS, axV, axT = define_axes(fig)

  # RGB color bar
  plot_colorbar(axRGB,[rgb_stretch(R, G, B, target)],ylabel = 'RGB')

  # hue color bar
  plot_colorbar(axH,[Hue], ylabel='hue')

  # saturation
  plot_timeseries(axS,t,dt,s,start,stop,ylabel='saturation')

  # value
  plot_timeseries(axV,t,dt,v,start,stop,ylabel='value')

  # delta temperatures
  plot_timeseries(axT,t,dt,dBT,start,stop,ylabel=r'$\Delta$T ($^{o}$C)',color='k')
  axT.set_xlabel('Year')

  # plt.show()

  # save
  outdir = '/home/sam/git/crater_lakes/plots/Kelimutu'
  if not os.path.exists(outdir):
    os.mkdir(outdir)
  os.chdir(outdir)
  plt.savefig(target+'_v6_temp.png')
  plt.close()
  print('saved: '+target)

def main():
  
  args = sys.argv[1:]

  if len(args) != 1:
    print('usage: python3 plot_time_series_v6.py {target_name}')
    return
  try:
    target = args[0]
    plotting_manager(target)
  except:
    print('problem running with :'+target)

if __name__ == '__main__':
  main()














