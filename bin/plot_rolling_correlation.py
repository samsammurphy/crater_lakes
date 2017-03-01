#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

plot_rolling_correlation.py

Created on Mon Feb 27 12:40:35 2017
@author: sam
"""

from read_excel_files import read_satellite_data


df = read_satellite_data('Yugama').resampled('1D')

hue = df['hue']

auto = hue.rolling(window=365).corr()

auto.plot()