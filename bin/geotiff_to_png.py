#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

geotiff_to_png.py

Created on Mon Mar  6 12:03:52 2017
@author: sam
"""

import gdal


fpath = '/home/sam/Downloads/kelimutu_rgb_test.tif'
dataset = gdal.Open(fpath)     

# Obtains a JPEG GDAL driver
pngDriver = gdal.GetDriverByName("png")   

# Create the .JPG file
pngDriver.CreateCopy("/home/sam/Downloads/kelimutu_rgb.png", dataset)  