# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 13:45:06 2016

@author: sam
"""

import ee

#wavebands names
bandNames = ['blue','green','red','nir','swir1','swir2']

def satellite_ID(img):
  fileID = ee.String(img.get('system:index'))
  satID = fileID.slice(0,3)
  return satID

# waveband numbers
def get_bandNums(satID):
  
  bandnums_dict = ee.Dictionary({
  'LT4':['B1','B2','B3','B4','B5','B7'],\
  'LT5':['B1','B2','B3','B4','B5','B7'],\
  'LE7':['B1','B2','B3','B4','B5','B7'],\
  'LC8':['B2','B3','B4','B5','B6','B7']
  })
  
  return bandnums_dict.get(satID)  

# spectral subset of an image
def spectral_subset(img):
  satID = satellite_ID(img)
  bandNums = get_bandNums(satID)
  img.select(bandNums,bandNames) \
    .set('satID',satID) \
    .set('bandNums',bandNums) \
    .set('bandNames',bandNames)

  return img

#at-sensor radiance
def toRad(img):
  rad = ee.Algorithms.Landsat.calibratedRadiance(img)
  return spectral_subset(rad)

#top-of-atmosphere reflectance
def toToa(img):
  toa = ee.Algorithms.Landsat.TOA(img)
  return spectral_subset(toa)

