# -*- coding: utf-8 -*-
"""
preprocess_LANDSAT.py, Sam Murphy (2016-10-24)

Basic preprocessing of LANDSAT satellite imagery (i.e. spectral subsets, 
renames bands, convert from DN to radiance/TOA)
"""

import ee


class Satellite():
  """
  Tests to see which satellite mission(s) this image belongs to
  """
    
  def ID(img):
    """
    Landsat satellite ID (i.e. first three letters of system:index)
    """
    return ee.String(img.get('system:index')).slice(0,3)
  
  def isL4or5(satID):
    """
    Is image from Landsat 4 or 5? (i.e. Thematic Mapper)
    """
    isL4 = satID.rindex('LT4').eq(0)
    isL5 = satID.rindex('LT5').eq(0)
    return isL4.Or(isL5)
    
  def isL7(satID):
    """
    Is image from Landsat 7? (i.e. Enhanced Thematic Mapper Plus)
    """
    return satID.rindex('LE7').eq(0)
    
  def isL8(satID):
    """
    Is image from Landsat 8? (i.e. Ocean-Land Imager and Thermal Imager)
    """
    return satID.rindex('LC8').eq(0)
    
    
# vnir spectral subset
def vnirNums(satID):
  return ee.Algorithms.If(Satellite.isL8(satID),['B2','B3','B4','B5'],['B1','B2','B3','B4'])
  
# swir spectral subset
def swirNums(satID):
  return ee.Algorithms.If(Satellite.isL8(satID),['B6','B7'],['B5','B7'])

# tir spectral subset
def tirNums(satID):
    
  dic = ee.Dictionary({
  'LT4':['B6'],\
  'LT5':['B6'],\
  'LE7':['B6_VCID_1','B6_VCID_2'],\
  'LC8':['B10','B11'],\
  })
  
  return dic.get(satID)

def tirNames(satID):
  return ee.Algorithms.If(Satellite.isL4or5(satID),['tir1'],['tir1','tir2'])
  
#at-sensor radiance
def toRad(img):
  rad = ee.Algorithms.Landsat.calibratedRadiance(img)
  satID = Satellite.ID(img)
  vnir = rad.select(vnirNums(satID),['blue','green','red','nir'])
  swir = rad.select(swirNums(satID),['swir1','swir2'])
  tir = rad.select(tirNums(satID),tirNames(satID))

  return ee.Dictionary({'vnir':vnir,'swir':swir,'tir':tir})

#top-of-atmosphere reflectance
def toToa(img):
  toa = ee.Algorithms.Landsat.TOA(img)
  satID = Satellite.ID(img)
  vnir = toa.select(vnirNums(satID),['blue','green','red','nir'])
  swir = toa.select(swirNums(satID),['swir1','swir2'])
  tir = toa.select(tirNums(satID),tirNames(satID))

  return ee.Dictionary({'vnir':vnir,'swir':swir,'tir':tir})
