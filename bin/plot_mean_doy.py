#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

plot_mean_doy.py

Plots mean value at day of year (or other sampling frequency)

Created on Wed Mar  1 20:58:16 2017
@author: sam
"""

import pandas as pd

# data
from read_excel_files import read_satellite_data
df = read_satellite_data('Yugama').df

 
#  if this_doy.any().all():
#    means.append(this_doy.mean())
#
#all_means = pd.concat(means).sort_index(axis=0)
#
#all_means.plot()


