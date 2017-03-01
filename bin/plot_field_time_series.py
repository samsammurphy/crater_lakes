#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

plot_field_time_series.py


Created on Tue Feb 28 16:44:31 2017
@author: sam
"""

from read_excel_files import read_field_data
import matplotlib.pylab as plt


def norm(df,varname):
  """
  Normalizes a variable by its maximum value
  """
  return df[varname] / df[varname].max()


# read the excel file
df = read_field_data('Yugama').df

# create 3 subplots
fig, (ax1, ax2, ax3) = plt.subplots(3,1, sharex = True)
fig.set_size_inches(9,9) 
plt.tight_layout(True)

# plot unrest (green) and eruption (red)
for ax in [ax1,ax2,ax3]:
  ax.stem(df['date'],df['unrest'],'#7f7f7f')   # grey
  ax.stem(df['date'],df['eruption'],'#d62728') # red

# plot pH and Cl
ax1.plot(norm(df,'pH'),label='pH')
ax1.plot(norm(df,'Cl'),label='Cl')
ax1.set_ylim(0.3,1)
ax1.legend()

# plot Ca, Na, K, Al
ax2.plot(norm(df,'Ca'),label='Ca')
ax2.plot(norm(df,'Na'),label='Na')
ax2.plot(norm(df,'K'),label='K')
ax2.plot(norm(df,'Al'),label='Al', color = '#9467bd')
ax2.legend()

# plot Fe, Mg
ax3.plot(norm(df,'Fe'),label='Fe')
ax3.plot(norm(df,'Mg'),label='Mg')
ax3.legend()


