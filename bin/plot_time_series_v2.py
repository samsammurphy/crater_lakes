#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_time_series_v3.py

Created on Fri Feb 10 16:25:34 2017

@author: sam
"""

import os
import numpy as np
import datetime
import time
import matplotlib.pylab as plt
from matplotlib.colors import  ListedColormap
import colorsys
from read_csv import read_csv



def interpolate_RGB(r,g,b,timestamps, start, stop):
  """
  Linear interpolation of (r,g,b) over given time period
  """
  numdays = (stop-start).days
  hires_dates = [start + datetime.timedelta(days=x) for x in range(0,numdays)]
  hires_time = [time.mktime(date.timetuple()) for date in hires_dates]
  
  # interpolate r,g,b
  R = np.interp(hires_time, timestamps, r)
  G = np.interp(hires_time, timestamps, g)
  B = np.interp(hires_time, timestamps, b)
  
  return list(zip(R,G,B))


# Data
targets = ['Azufral','Chichon_El','Copahue','Ijen','Kelimutu_a','Kelimutu_b','Kelimutu_c','Poas','Rincon_de_la_Vieja','Ruapehu','Yugama']

for target in targets:
  
  print(target)
  
  D = read_csv(target)
  
  # set time period
  start = datetime.datetime(1985,1,1)
  stop  = datetime.datetime(2016,1,1) 
  
  # Interpolate RGB over time period
  RGB = interpolate_RGB(D['r'],D['g'],D['b'],D['timestamps'],start,stop)
  
  # Linear strech
  stretched_RGB = np.array(RGB) * 1/np.max(RGB)
  
  # figure
  fig = plt.figure(figsize=(8,12))
  
  # size of figure components
  plot_height = 0.3
  bar = 0.12
  gap = 0.05
  minigap = 0.02
  
  # plot r,g,b, trendlines
  axplot = fig.add_axes([0.07,gap+plot_height+4*minigap+2*bar,0.90,plot_height])
  axplot.plot(D['datetimes'],D['r'],'r-o')
  axplot.plot(D['datetimes'],D['g'],'g-o')
  axplot.plot(D['datetimes'],D['b'],'b-o')
  axplot.set_xlim(start,stop)
  axplot.set_ylim(0,1)
  axplot.set_ylabel('reflectance')
  
  # visualize rgb
  axRGB = fig.add_axes([0.07,gap+plot_height+2*minigap+bar,0.9,bar])
  axRGB.imshow([RGB], interpolation='nearest', aspect='auto') #stretches rgb to fit axes
  axRGB.set_xticks([])
  axRGB.set_yticks([])
  
  # linear stretch rgb
  #stretched_RGB
  axRGB = fig.add_axes([0.07,gap+plot_height+minigap,0.9,bar])
  axRGB.imshow([stretched_RGB], interpolation='nearest', aspect='auto') #stretches rgb to fit axes
  axRGB.set_xticks([])
  axRGB.set_yticks([])
  
  # plot delta temperatures
  axT = fig.add_axes([0.07,gap,0.9,plot_height])
  axT.plot(D['datetimes'],D['dT'],'k-o')
  axT.set_xlabel('Year')
  axT.set_ylabel(r'$\Delta$T ($^{o}$C)')
  
  # save
  outdir = '/home/sam/git/crater_lakes/plots/'+target
  if not os.path.exists(outdir):
    os.mkdir(outdir)
  os.chdir(outdir)
  plt.savefig(target+'_v2.png')
  plt.close()
  





