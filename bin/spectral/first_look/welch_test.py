#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

welch_test.py

Created on Wed Feb 22 15:15:54 2017
@author: sam
"""

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


# Plot sine wave
freq = 10 # frequency of sine wave
fs = 100  # sampling frequency
N = 200   # number of samples in total
time = np.arange(N) / fs
x = 2*np.sin(2*np.pi*freq*time)
plt.plot(x)
plt.show()


random_filter = np.random.choice([0, 1], size=(len(x),),p=[1./4,3./4])
for i, r in enumerate(random_filter):
  if not r:
    x[i] = np.NaN

plt.plot(x)
plt.show()


#Plot the power spectral density.
f, Pxx = signal.welch(x, fs, nperseg=365) # f = array of sample frequencies, Pxx = power spectral density
plt.semilogy(f, Pxx)
plt.xlabel('frequency')
plt.ylabel('Power Spectral Density')
plt.show()

