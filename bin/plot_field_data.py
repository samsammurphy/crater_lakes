#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

plot_field_data.py

Created on Thu Feb 16 15:47:59 2017
@author: sam
"""


import pandas as pd
import matplotlib.pylab as plt


target = 'Rincon_de_la_Vieja'
var = 'SO4'


df = pd.read_excel('/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/'
                   'data/{0}/{0}_field.xlsx'.format(target))

plt.plot(df['date'],df[var],'-')
plt.plot(df['date'],df[var],'.')
plt.title(var)

plt.savefig('/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/data/{0}/'
            'field_timeseries/{0}_{1}.png'.format(target,var))