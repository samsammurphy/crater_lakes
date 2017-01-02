# -*- coding: utf-8 -*-
"""
preprocess.py, Sam Murphy (2016-10-24)

Basic preprocessing of satellite imagery (i.e. spectral subsets, renames bands,
convert from DN to radiance/TOA)
"""

import ee


# satellite ID
def satellite_ID(img):

  # first three letters of GEE 'filename' (i.e. system:index)
  prefix = ee.String(img.get('system:index')).slice(0,3)
  
  # is the first letter 'L'?
  strCompare = prefix.slice(0,1).compareTo('L') 
  # NOTE! compareTo() will return ZERO if comparison is TRUE!!
  
  # if yes return prefix (i.e. Landsat) else return 'AST' (i.e. ASTER)                                      
  return ee.Algorithms.If(strCompare, 'AST', prefix)
  # !! i.e. prefix is in 'false' position of ee.Algorithms.If() because, in
  # this special case, ZERO = TRUE !!
  
  
# visible-to-shortwave band names
def get_vswirNames(satID):
  
  vswirNames_dict = ee.Dictionary({
  'LT4':['blue','green','red','nir','swir1','swir2'],\
  'LT5':['blue','green','red','nir','swir1','swir2'],\
  'LE7':['blue','green','red','nir','swir1','swir2'],\
  'LC8':['blue','green','red','nir','swir1','swir2'],\
  'AST':['green','red','nir','swir1','swir2','swir3','swir4','swir5','swir6']
  # ASTER does not have a blue band, i.e. B01 = green
  })
  
  return vswirNames_dict.get(satID)

# visible-to-shortwave band numbers
def get_vswirNums(satID):
  
  vswirNums_dict = ee.Dictionary({
  'LT4':['B1','B2','B3','B4','B5','B7'],\
  'LT5':['B1','B2','B3','B4','B5','B7'],\
  'LE7':['B1','B2','B3','B4','B5','B7'],\
  'LC8':['B2','B3','B4','B5','B6','B7'],\
  'AST':['B01','B02','B3N','B04','B05','B06','B07','B08','B09']
  })
  
  return vswirNums_dict.get(satID)

# thermal infrared band names
def get_tirNames(satID):
  
  tirNames_dict = ee.Dictionary({
  'LT4':['tir1'],\
  'LT5':['tir1'],\
  'LE7':['tir1','tir2'],\
  'LC8':['tir1','tir2'],\
  'AST':['tir1','tir2','tir3','tir4','tir5']
  })
  
  return tirNames_dict.get(satID)
  
# thermal band numbers
def get_tirNums(satID):
  
  tirNums_dict = ee.Dictionary({
  'LT4':['B6'],\
  'LT5':['B6'],\
  'LE7':['B6_VCID_1','B6_VCID_2'],\
  'LC8':['B10','B11'],\
  'AST':['B10','B11','B12','B13','B14']
  })
  
  return tirNums_dict.get(satID)
  
# vswir spectral subset
def vswir_subset(img, satID):
  vswirNums = ee.List(get_vswirNums(satID))
  vswirNames = ee.List(get_vswirNames(satID))
  subset = img.select(vswirNums,vswirNames)\
    .set('satID',satID)\
    .set('vswirNums',vswirNums)\
    .set('vswirNames',vswirNames)
  return subset

# tir spectral subset
def tir_subset(img, satID):
  tirNums = get_tirNums(satID)
  tirNames = get_tirNames(satID)
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

