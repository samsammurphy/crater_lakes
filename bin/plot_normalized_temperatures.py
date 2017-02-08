#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

plot_normalized_temperatures.py

Created on Tue Feb  7 18:44:17 2017
@author: sam
"""


import os
import numpy as np
import matplotlib.pylab as plt
import datetime

# load datA
os.chdir('/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/data/Poas/spreadsheets')
timestamp,dBT_norm,TFIELD_norm = np.genfromtxt('Poas_normalized_temperatures.csv',\
                                               delimiter=',',unpack=True,skip_header=1)

# plot
datetimes = [datetime.datetime.fromtimestamp(t) for t in timestamp]
plt.plot(datetimes,dBT_norm,'k-o')
plt.plot(datetimes,TFIELD_norm,'r-D')
plt.xlabel('year')
plt.ylabel('normalized temperatures')

