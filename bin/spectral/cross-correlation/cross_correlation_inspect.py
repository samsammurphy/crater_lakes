#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 11:50:08 2017

@author: sam
"""

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt



# 'continuous' frequency
c = 100

# sampling frequency is the number of data points in the signal
# i.e. 8 data points in this case..

# a signal 1
sig1 = np.repeat([0., 1., 1., 0., 1., 0., 0., 1.], c)

# slightly delayed version of signal 1
sig2 = np.repeat([1., 1., 0., 1., 0., 0., 1., 0.], c)


corr = signal.correlate(sig1, sig2, mode='same') / c


clock = np.arange(0, len(sig1), c)
fig, (ax_sig1, ax_sig2, ax_corr) = plt.subplots(3, 1, sharex=True)

ax_sig1.plot(sig1)
ax_sig1.plot(clock, sig1[clock], 'ro')
ax_sig1.set_title('Signal 1')

ax_sig2.plot(sig2)
ax_sig2.plot(clock, sig2[clock], 'ro')
ax_sig2.set_title('Signal 2')

ax_corr.plot(corr)
ax_corr.plot(clock, corr[clock], 'ro')
ax_corr.axhline(0.5, ls=':')
ax_corr.set_title('Cross-correlation')
ax_corr.set_xlabel('Time (seconds)')
ax_sig1.margins(0, 0.1)
fig.tight_layout()
fig.show()


max_corr = np.where(corr == np.max(corr))[0]
time_of_maxcorr = clock[np.where(clock == max_corr)]

total_time = len(sig1)
delay = time_of_maxcorr - total_time/2

print('Signal 1 is {:.1f} seconds ahead of signal 2'.format(delay[0]))