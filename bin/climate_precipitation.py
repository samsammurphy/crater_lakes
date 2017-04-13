#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
climate_precipitation.py

Created on Tue Mar 21 13:06:12 2017
@author: sam
"""

import pandas as pd
import matplotlib.pylab as plt

# load data
df = pd.read_csv('/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/Kelimutu/climate/satellite/precipitation_history.csv',\
                 parse_dates = ['system:index'])

# set time index
df = df.set_index(pd.DatetimeIndex(df['system:index']))

# time slice
start = df.index.searchsorted(pd.datetime(2013,7,1))
stop = df.index.searchsorted(pd.datetime(2015,7,1))
df = df.ix[start:stop]

monthly = df.resample('1M').agg('sum')

fig = plt.figure(figsize=(24,12))
plt.plot(monthly.precipitation,'--')
plt.plot(monthly.precipitation,'r*')
plt.xlabel('Date')
plt.ylabel('Precipitation (mm)')


plot_date_lines = False

if plot_date_lines:
    plt.axvline(pd.datetime(2013,10,6),color='magenta')
    plt.axvline(pd.datetime(2013,11,7),color='magenta')
    plt.axvline(pd.datetime(2014,1,26),color='magenta')
    plt.axvline(pd.datetime(2014,3,23),color='magenta')
    plt.axvline(pd.datetime(2014,3,31),color='magenta')
    
    plt.axvline(pd.datetime(2014,6,19),color='magenta')
    plt.axvline(pd.datetime(2014,7,21),color='magenta')
    plt.axvline(pd.datetime(2014,10,9),color='magenta')
    plt.axvline(pd.datetime(2014,11,10),color='magenta')
    plt.axvline(pd.datetime(2015,1,29),color='magenta')
    plt.axvline(pd.datetime(2015,3,10),color='magenta')

plt.show()