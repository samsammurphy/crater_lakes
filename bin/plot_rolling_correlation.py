#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

my_autocorrelation.py

Created on Mon Feb 27 12:40:35 2017
@author: sam
"""

from read_excel_files import read_satellite_data
import matplotlib.pylab as plt
import pandas as pd


target = 'Kelimutu_b'

# satellite and field data
sat = read_satellite_data(target).resampled('1D')

# calculate rolling autocorrelation
hue = sat['hue']['1990':'2000']
offset = pd.tseries.offsets.Day(n=365*2)
auto = hue.rolling(window=offset).apply(hue.autocorr(lag=365))

# plot
fig, (ax1, ax2) = plt.subplots(2,1, sharex = True)
ax1.plot(hue)
ax2.plot(auto)


