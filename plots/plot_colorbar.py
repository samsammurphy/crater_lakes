#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

plot_colorbar.py

The idea here is to plot the 'best guess' for lake colour
through time in a 24-bit colour bar..

so that the reader can see what the RGB and HSV plots equate
to..

Created on Mon Feb  6 15:16:39 2017
@author: sam
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# interpolated RGB arrays (i.e. no data gaps)
r = np.linspace(0,255,256)
g = np.linspace(0,0,256)
b = np.linspace(255,0,256)

# need to reverse (hopefully not required with actual data)
r = r[::-1]
g = g[::-1]
b = b[::-1]

# zip it up
arr = np.array(list(zip(r,g,b)))

# repeat over a bunch of 'rows'
img = []
for i in range(100):
  img.append(arr)

# display
plt.imshow(img)
plt.axis("off")
plt.show()