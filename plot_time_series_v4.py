#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

plot_time_series_v2.py

Created on Mon Feb  6 20:53:54 2017
@author: sam
"""
import os
import pandas as pd
import numpy as np
import datetime
import time
import matplotlib.pylab as plt
from matplotlib.colors import  ListedColormap
import colorsys


def null_handler(df):
  """
  Handles missing data values
  """
  
  # define ok as red = True
  ok = np.array([~pd.isnull(df['red'])])[0]
  
  # filter arrays
  r = df['red'][ok]
  g = df['green'][ok]
  b = df['blue'][ok]
  h = df['hue'][ok]
  s = df['saturation'][ok]
  v = df['value'][ok]
  t = df['timestamp'][ok]
  
  # handle full and filtered datetime separately 
  DT = np.array([datetime.datetime.fromtimestamp(t) for t in df['timestamp']])
  dt = DT[ok]
  
  return (r,g,b,h,s,v,t,dt,DT)
  

def interpolate_triplet(r,g,b,timestamps, start, stop):
  """
  Linear interpolation of color triplet over given time period
  """
  numdays = (stop-start).days
  hires_dates = [start + datetime.timedelta(days=x) for x in range(0,numdays)]
  hires_time = [time.mktime(date.timetuple()) for date in hires_dates]
  
  # interpolate r,g,b
  R = np.clip(np.interp(hires_time, timestamps, r),0,1)
  G = np.clip(np.interp(hires_time, timestamps, g),0,1)
  B = np.clip(np.interp(hires_time, timestamps, b),0,1)
  
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


target = 'Ruapehu'
  
# read excel file
df = pd.read_excel('/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/data/{0}/{0}.xlsx'.format(target))

# null handler
r,g,b,h,s,v,t,dt,DT = null_handler(df)

# time period define
start = datetime.datetime(1985,1,1)
stop  = datetime.datetime(2016,1,1) 

# interpolate
RGB = interpolate_triplet(r,g,b,t,start,stop)
HSV = interpolate_triplet(h,s,v,t,start,stop)

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
axplot.plot(dt,r,'r-o')
axplot.plot(dt,g,'g-o')
axplot.plot(dt,b,'b-o')
axplot.set_xlim(start,stop)
axplot.set_ylim(0,1)
axplot.set_ylabel('reflectance')

# visualize rgb
stretched_RGB = np.array(RGB) * 1/np.max(RGB)
axRGB = fig.add_axes([0.07,plot_height+gap+4*mini_gap+3*minibar,0.9,bar])
axRGB.imshow([stretched_RGB], interpolation='nearest', aspect='auto') #stretches rgb to fit axes
axRGB.set_xticks([])
axRGB.set_yticks([])

# visualize hue
hue = [colorsys.hsv_to_rgb(x[0],1,1) for x in HSV]# use max. saturation and value
axH = fig.add_axes([0.07,plot_height+gap+3*mini_gap+2*minibar,0.9,minibar])
axH.imshow([hue], interpolation='nearest', aspect='auto') 
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
axT.plot(DT,df['dBT'],'k-o')
axT.set_xlabel('Year')
axT.set_ylabel(r'$\Delta$T ($^{o}$C)')
axT.set_xlim(start,stop)

# save
outdir = '/home/sam/git/crater_lakes/plots/'+target
if not os.path.exists(outdir):
  os.mkdir(outdir)
os.chdir(outdir)
#plt.savefig(target+'_v4.png')
#plt.close()

















