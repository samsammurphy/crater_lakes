#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

plot_all.py

Plots all the output from a Crater Lake target

Created on Mon Feb  6 20:53:54 2017
@author: sam
"""

import matplotlib.pylab as plt
import datetime
from load_atmcorr import load_plot_data
from plot_RGB import plot_RGB
from plot_color_timeseries import plot_color_timeseries
from plot_greyness_and_value import plot_greyness_and_value
from plot_dT import plot_dT
import os

# all targets
#f = open('/home/sam/Dropbox/HIGP/Crater_Lakes/z/Volcanoes/volcano_names.txt')
#for line in f:
#  target = line.rstrip()

for target in ['Lake_Nyos']:

  # figure with subplots
  fig = plt.figure(figsize=(8,12))
  ax1 = fig.add_subplot(4,1,1) # four rows, one column, first plot                   
  ax2 = fig.add_subplot(4,1,2) 
  ax3 = fig.add_subplot(4,1,3) 
  ax4 = fig.add_subplot(4,1,4)
  
  # time period
  start = datetime.datetime(1985,1,1)
  stop  = datetime.datetime(2016,1,1)   
  
  # load data
  data = load_plot_data(target)
  
  # plot
  plot_RGB(ax1, data, start, stop)
  plot_color_timeseries(ax2, data, start, stop, 10)
  plot_greyness_and_value(ax3, data, start, stop)
  plot_dT(ax4, data, start, stop)
  
  
  outdir = '/home/sam/git/crater_lakes/plots/'+target
  if not os.path.exists(outdir):
    os.mkdir(outdir)
  os.chdir(outdir)
  plt.savefig(target+'.png')
  plt.show()
#  plt.close(fig)