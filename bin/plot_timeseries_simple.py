#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_timeseries_simple.py

Created on Tue Feb 14 16:06:46 2017

@author: sam
"""

import pandas as pd
import datetime
import matplotlib.pylab as plt
import re

target = 'Yugama'
var = 'Al/Mg'

df = pd.read_excel('/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/data/{0}/{0}.xlsx'.format(target))
dt = [datetime.datetime.fromtimestamp(t) for t in df['timestamp']]

plt.title(var)
plt.plot(dt,df[var])
plt.plot(dt,df[var],'.')


# save
outdir = '/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/data/{}/timeseries'.format(target)
plt.savefig('{0}/{1}_{2}.png'.format(outdir,target,re.sub('/','_',var)))

