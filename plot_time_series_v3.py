#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

plot_time_series_v2.py

Created on Mon Feb  6 20:53:54 2017
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



def grey_magenta_cmap():
  """
  Creates a color map from grey to magenta for saturation visualization
  """
  
  color_list = []
  
  for alpha in np.linspace(0,1,101):
    grey_component = np.array([g*(1-alpha) for g in (0.5,0.5,0.5)])
    magenta_component = np.array([m*alpha for m in (1,0,1)])
    color_list.append(grey_component+magenta_component)
    
  return ListedColormap(color_list, name='from_list')



# Data
targets = ['Yugama']

for target in targets:
  
  print(target)
  
  D = read_csv(target)
  
  # set time period
  start = datetime.datetime(1985,1,1)
  stop  = datetime.datetime(2005,1,1) 
  
  # Interpolate RGB over time period
  RGB = interpolate_RGB(D['r'],D['g'],D['b'],D['timestamps'],start,stop)
  
  # Calculate HSV for interpolated RGB values
  HSV = [colorsys.rgb_to_hsv(x[0],x[1],x[2]) for x in RGB]
  
  # figure
  fig = plt.figure(figsize=(8,12))
  
  # size of figure components
  plot_height = 0.3
  bar = 0.12
  minibar = 0.03
  gap = 0.05
  mini_gap = 0.02
  
  # plot r,g,b, trendlines
  axplot = fig.add_axes([0.07,plot_height+gap+6*mini_gap+3*minibar+bar,0.90,plot_height])
  axplot.plot(D['datetimes'],D['r'],'r-o')
  axplot.plot(D['datetimes'],D['g'],'g-o')
  axplot.plot(D['datetimes'],D['b'],'b-o')
  axplot.set_xlim(start,stop)
  axplot.set_ylim(0,1)
  axplot.set_ylabel('reflectance')
  
  # visualize rgb
  axRGB = fig.add_axes([0.07,plot_height+gap+4*mini_gap+3*minibar,0.9,bar])
  axRGB.imshow([RGB], interpolation='nearest', aspect='auto') #stretches rgb to fit axes
  axRGB.set_xticks([])
  axRGB.set_yticks([])
  
  # visualize hue (using saturation = 1 and value = 1)
  hue = [x[0] for x in HSV]
  H = [colorsys.hsv_to_rgb(h,1,1) for h in hue]
  axH = fig.add_axes([0.07,plot_height+gap+3*mini_gap+2*minibar,0.9,minibar])
  axH.imshow([H], interpolation='nearest', aspect='auto',cmap='plasma') 
  axH.set_xticks([])
  axH.set_yticks([])
  
  # visualize saturation
  axS = fig.add_axes([0.07,plot_height+gap+2*mini_gap+minibar,0.9,minibar])
  axS.imshow([[x[1] for x in HSV]], interpolation='nearest', aspect='auto',cmap=grey_magenta_cmap()) 
  axS.set_xticks([])
  axS.set_yticks([])
  
  # visualize value
  axV = fig.add_axes([0.07,plot_height+gap+mini_gap,0.9,minibar])
  axV.imshow([[x[2] for x in HSV]], interpolation='nearest', aspect='auto',cmap='plasma') 
  axV.set_xticks([])
  axV.set_yticks([])
  
  # plot delta temperatures
  axT = fig.add_axes([0.07,gap,0.9,plot_height])
  axT.plot(D['datetimes'],D['dT'],'k-o')
  axT.set_xlabel('Year')
  axT.set_ylabel(r'$\Delta$T ($^{o}$C)')
  axT.set_xlim(start,stop)
  
  # save
  outdir = '/home/sam/git/crater_lakes/plots/'+target
  if not os.path.exists(outdir):
    os.mkdir(outdir)
  os.chdir(outdir)
  #plt.savefig(target+'_v3.png')
  #plt.close()

















