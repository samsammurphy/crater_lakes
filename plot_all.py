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
from load_atmcorr import chronological_data
from plot_RGB import plot_RGB
from plot_HSV import plot_HSV
from plot_dT import plot_dT
from plot_color_timeseries import plot_color_timeseries



# load data
target = 'Poas'
data = chronological_data(target)            
                    
# figure with subplots
fig = plt.figure(figsize=(8,12))
ax1 = fig.add_subplot(4,1,1) # two rows, one column, first plot
ax2 = fig.add_subplot(4,1,2) # two rows, one column, first plot
ax3 = fig.add_subplot(4,1,3) # two rows, one column, first plot
ax4 = fig.add_subplot(4,1,4) # two rows, one column, first plot

# time period
start = datetime.datetime(2000,1,1)
stop  = datetime.datetime(2016,1,1)        

# rgb
plot_RGB(ax1, data, start, stop)

# colorbar
plot_color_timeseries(ax2, data, start, stop)

# hsv
plot_HSV(ax3, data, start, stop)

# dT
plot_dT(ax4, data, start, stop)
