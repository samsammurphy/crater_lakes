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
start = df.index.searchsorted(pd.datetime(2012,7,1))
stop = df.index.searchsorted(pd.datetime(2016,7,1))
df = df.ix[start:stop]

monthly = df.resample('1M').agg('sum')

plt.plot(monthly.precipitation,'*-')
plt.xlabel('Date')
plt.ylabel('Precipitation (mm)')
plt.show()