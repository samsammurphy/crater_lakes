# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 13:45:06 2016

@author: sam
"""

import ee

#wavebands names
band_names = ['blue','green','red','nir','swir1','swir2']

# waveband nums
def get_band_nums(img):
  L4_to_L7 = ['B1','B2','B3','B4','B5','B7']
  L8 = ['B2','B3','B4','B5','B6','B7']
  
  # TODO check out 'inspect_LEDAPS_SR' for a better way to do this
  # will make it easier when parsing out the TIR wavebands
  # and also to handle ASTER data when available  
  
  SPACECRAFT_ID = ee.String(img.get('SPACECRAFT_ID'))
  band_nums = ee.Algorithms.If(SPACECRAFT_ID.index(ee.String('LANDSAT_8')).neq(-1), L8, L4_to_L7)
  return band_nums

#at-sensor radiance
def toRad(img):
  rad = ee.Algorithms.Landsat.calibratedRadiance(img)
  band_nums = get_band_nums(img)
  return rad.select(band_nums,band_names)

#top-of-atmosphere reflectance
def toToa(img):
  toa = ee.Algorithms.Landsat.TOA(img)
  band_nums = get_band_nums(img)
  return toa.select(band_nums,band_names)

