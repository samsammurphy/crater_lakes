#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 15:46:54 2017

@author: sam
"""

import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from read_excel_files import read_satellite_data
from plot_field_time_series import plot_unrest_and_eruptions

# data
varname = 'dBT'
df = read_satellite_data('Yugama').resampled('1D')['1990':'2010']
s = df[varname]
d = s.index

# rolling autocorrelation
lag = 365
autocorr = []

for pos in range(lag*2,len(s)):
  x1 = s[pos-lag:pos]
  x2 = s[pos-2*lag:pos-lag]
  corr = np.corrcoef(x1,x2)[1][0]
  autocorr.append(corr)

# concat into series
result = pd.Series(data=autocorr,index=d[lag*2:])

# plot
fig, (ax1,ax2) = plt.subplots(2,1,sharex=True)
ax1.set_title('autocorrelation (k=1Y,overlap=0)')
ax1.plot(s)
ax1.set_ylabel(varname)
plot_unrest_and_eruptions(ax1)
#ax1.axvline(x=d[pos-lag],color='#7f7f7f')
#ax1.axvline(x=d[pos],color='#d62728')

ax2.plot(result)
ax2.set_ylabel('autocorrelation')
#ax2.set_xlim((pd.datetime(1990,1,1),pd.datetime(2000,1,1)))