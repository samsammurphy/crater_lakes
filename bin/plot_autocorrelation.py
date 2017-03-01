#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

plot_autocorrelation.py

Created on Tue Feb 28 11:39:06 2017
@author: sam
"""



from read_excel_files import read_satellite_data

df = read_satellite_data('Yugama').resampled('1D')



auto = df['hue'].autocorr()

print(auto)