# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 14:44:09 2016

@author: sam
"""

import gdal
import numpy as np
from scipy.misc import bytescale
import matplotlib.pylab as plt
import sys


# image file path
fpath = '/home/sam/Downloads/test7.tif'

# open a file
ds = gdal.Open(fpath)

# array
arr = np.array(ds.GetRasterBand(1).ReadAsArray())

# handle NaNs
good = np.where(arr==arr)
bad  = np.where(arr!=arr)
if len(good) != 2:
  sys.exit()
if len(bad) == 2:
  arr[bad] = np.min(arr[good])

# greyscale image
img = bytescale(arr)

# display image
plt.imshow(img)
plt.show()

# statitcs
print(np.min(arr))
print(np.max(arr))