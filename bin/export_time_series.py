#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
export_time_series.py

Created on Sat Feb  4 09:17:54 2017
@author: sam
"""

import ee
from preprocess_ASTER import Aster
from masks import Mask
from lake_analyses import LakeAnalysis
from atmospheric import Atmospheric
import preprocess_LANDSAT
from LEDAPS import Ledaps

def color_metrics(toa):
    """
    Calculates 
    
    - (new) 2D 'saturation' and 'value' of red-green space, and
    - (traditional) 3D Hue-Saturation-Value IF blue band available.
    
    """
    
    # 2D color: ASTER & LANDSAT
    R = ee.Image(toa).select(['red'])
    G = ee.Image(toa).select(['green'])
    saturation = R.subtract(G).abs()
    value = R.max(G)
    metrics = ee.Dictionary({'2D':
                                ee.Dictionary({'saturation':saturation,'value':value})
                            })
    
    # 3D color
    hasBlue = ee.List(ee.Image(toa).bandNames()).contains('blue')
    HSV = ee.Algorithms.If(hasBlue,\
      ee.Image(toa).select(['red','green','blue']).rgbToHsv(),'null')
    metrics = ee.Dictionary(metrics).set('3D',HSV)
        
    return metrics


class brightnessTemperature():
  
  def ASTER(rad):
    BTs = Aster.temperature.fromRad(rad)# all BTs (for each TIR waveband)
    BT14 = ee.Image(BTs).select('BT14') # just band 14 (11.3 microns) 
    
    return(BT14)

  def Landsat(toa):
    
    BT = ee.Image(ee.Dictionary(toa).get('tir')).select('tir1') 
  
    return BT
  

class preprocess():
  
  def ASTER(img):
    
    rad = Aster.radiance.fromDN(img)     # at-sensor radiance
    toa = Aster.reflectance.fromRad(rad) # top of atmosphere reflectance
    BT  = brightnessTemperature(rad)     # brightness temperature, single band
    
    return (rad, toa, BT)

  def Landsat(img):

    rad = preprocess_LANDSAT.toRad(img) 
    toa = preprocess_LANDSAT.toToa(img) 
    BT  = brightnessTemperature(toa)
    
    return (rad, toa, BT)

# extracts data from an image (will be mapped over collection)
def extraction(geom):
  """
  A closure to hold target geometry when mapped over image colleciton
  """
  
  def extract_data(img):
    """
    Preprocesses scenes, applies masks, extracts radiance data and pixel counts
    """
     
    rad, toa, BT = ee.Algorithms.If(ee.List([sat]).contains('AST'),preprocess.ASTER(img),preprocess.Landsat(img))
    
    # vnir color metrics
    color = color_metrics(toa.get('vnir'))
      
    # cloud mask
    cloud = Mask.cloud(color, BT)
    
    # water mask
    water = Mask.water(toa.get('vnir')) 
      
    # lake analyses
    vnir = LakeAnalysis.vnir(rad,geom,cloud,water,BT)
    swir = LakeAnalysis.swir(rad,geom,cloud,water,BT)
    tir = LakeAnalysis.tir(rad,geom,cloud,water)
    
    # date and time
    date = ee.Date(img.get('system:time_start'))
    jan01 = ee.Date.fromYMD(date.get('year'),1,1)
    doy = date.difference(jan01,'day').add(1)
  
    result = ee.Dictionary({
                            'date':date,
                            'doy':doy,
                            'vnir':vnir,
                            'swir':swir,
                            'tir':tir,
                            'solar_z':ee.Number(90.0).subtract(img.get('SOLAR_ELEVATION')),
                            'H2O':Atmospheric.water(geom,date),
                            'O3':Atmospheric.ozone(geom,date)
                            })

    return ee.Feature(geom,result)
    
  return extract_data