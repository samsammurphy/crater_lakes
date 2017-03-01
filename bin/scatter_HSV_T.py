#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

scatter_HSV_T.py

Created on Tue Feb 28 14:04:48 2017
@author: sam
"""

from read_excel_files import read_satellite_data
import matplotlib.pylab as plt


# read excel file
df = read_satellite_data('Yugama').df
                        
# group by month
grouped = df.groupby(df.index.month)


"""
TODO!

Dataframe slicing makes this a since, you can pass it logical operators!!


in_season = ddf[(ddf.index.month > 1) & (ddf.index.month <= 3)]

"""

# define seeasons and coloration
seasons = {
    'spring':([3,4,5],'#2ca02c'), # green
    'summer':([6,7,8],'#bcbd22'), # yellow      
    'autumn':([9,10,11],'#d62728'),
    'winter':([12,1,2],'#1f77b4')
    }

# define 6 plot pairs
pairs = [('saturation','value'),\
         ('saturation','dBT'),\
         ('value','dBT'),\
         ('hue','saturation'),\
         ('hue','value'),\
         ('hue','dBT')]

# create 6 subplots
fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3)
fig.set_size_inches(9, 5)
plt.tight_layout(True)

# do plotting 
for i, ax in enumerate([ax1,ax2,ax3,ax4,ax5,ax6]):
  
  for season in ['spring','summer','autumn','winter']:
    
    months, color = seasons[season]
    
    for month in months:
  
      try:
        
        monthly = grouped.get_group(month)
      
        xname = pairs[i][0]
        yname = pairs[i][1]
        
        ax.scatter(monthly[xname],monthly[yname],color=color,marker='o')
        ax.set_xlabel(xname)
        ax.set_ylabel(yname)
        ax.set_xlim(0,1)
        ax.set_ylim(0,1)
        
        if yname == 'dBT':
          ax.set_ylim(-10,10)
    
      except:
        
        pass
