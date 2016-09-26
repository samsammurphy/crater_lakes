# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 13:45:06 2016

@author: sam
"""

import ee


def satellite_ID(img):
  return ee.String(img.get('system:index')).slice(0,3)
  
# visible-to-shortwave band names
def get_vswirNames(satID):
  
  vswirNames_dict = ee.Dictionary({
  'LT4':['blue','green','red','nir','swir1','swir2'],\
  'LT5':['blue','green','red','nir','swir1','swir2'],\
  'LE7':['blue','green','red','nir','swir1','swir2'],\
  'LC8':['blue','green','red','nir','swir1','swir2']
  })
  
  return vswirNames_dict.get(satID)

# visible-to-shortwave band numbers
def get_vswirNums(satID):
  
  vswirNums_dict = ee.Dictionary({
  'LT4':['B1','B2','B3','B4','B5','B7'],\
  'LT5':['B1','B2','B3','B4','B5','B7'],\
  'LE7':['B1','B2','B3','B4','B5','B7'],\
  'LC8':['B2','B3','B4','B5','B6','B7']
  })
  
  return vswirNums_dict.get(satID)

# spectral subset of vswir bands
def vswir_subset(img, satID):
  vswirNums = ee.List(get_vswirNums(satID))
  vswirNames = ee.List(get_vswirNames(satID))
  subset = img.select(vswirNums,vswirNames)\
    .set('satID',satID)\
    .set('vswirNums',vswirNums)\
    .set('vswirNames',vswirNames)
  return subset

# thermal band numbers
def get_tirNums(satID):
  
  tirNums_dict = ee.Dictionary({
  'LT4':['B6'],\
  'LT5':['B6'],\
  'LE7':['B6_VCID_1','B6_VCID_2'],\
  'LC8':['B10','B11']
  })
  
  return tirNums_dict.get(satID)

def tir_subset(img, satID):
  
  tirNums = get_tirNums(satID)
  tirNames = ee.Algorithms.If(ee.List(tirNums).length().eq(1),['tir1'],['tir1','tir2'])
  
  subset = img.select(tirNums,tirNames)\
    .set('satID',satID)\
    .set('tirNums',tirNums)\
    .set('tirNames',tirNames)
  
  return subset

#at-sensor radiance
def toRad(img):
  satID = satellite_ID(img)
  rad = ee.Algorithms.Landsat.calibratedRadiance(img)
  vswir = vswir_subset(rad, satID)
  tir = tir_subset(rad,satID)
  return vswir.addBands(tir)

#top-of-atmosphere reflectance
def toToa(img):
  satID = satellite_ID(img)
  toa = ee.Algorithms.Landsat.TOA(img)
  vswir = vswir_subset(toa, satID) 
  tir = tir_subset(toa,satID)
  return vswir.addBands(tir)

