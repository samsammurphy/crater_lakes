#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

time_grouping.py

Created on Wed Mar  1 21:41:29 2017
@author: sam
"""


import pandas as pd
import matplotlib.pylab as plt

# data
from read_excel_files import read_satellite_data
df = read_satellite_data('Yugama').df['1990':'2010']['hue']


# group by
for freq in ['D','M','3M','6M']:
  grouped = df.groupby(pd.TimeGrouper(freq)).mean()
  plt.plot(grouped,'.-')
  plt.title('GroupBy')
plt.show()

# resampling (is the same thing)
for freq in ['D','M','3M','6M']:
  resampled = df.resample(freq).agg('mean')
  plt.plot(resampled,'.-')
  plt.title('Resampled')
 