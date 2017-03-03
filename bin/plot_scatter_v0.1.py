#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

plot_scatter.py

Created on Mon Feb 13 19:01:40 2017
@author: sam
"""

import pandas as pd
import matplotlib.pylab as plt


x = 'T'
y = 'T'

# opens excel file
df = pd.read_excel('/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/data/Yugama/Yugama.xlsx')

# scatter plots two named variables
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

def simple_pair(x,y):
  ax.scatter(df[x],df[y])
  ax.set_xlabel(x)
  ax.set_ylabel(y)

  

simple_pair(x,y)
