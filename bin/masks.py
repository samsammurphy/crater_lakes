#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
masking.py, Sam Murphy 2017-01-10

Mask object used to define: clouds, water and valid TIR pixels 

Part of crater lakes project.
"""

import ee

class Mask():
  """
  Finds cloud, water and valid TIR pixels
  """
 
  def cloud(color, BT):
    """
    Cloud pixels are grey, bright and cold
    
    - grey and bright: 2D Saturation and Value
    - cold: Brightness Temperature
    
    More detail on grey and bright threshold:
    - Saturation always < 0.1
    - if Value between 0.1 and 0.2 then Saturation must be 0.1 less than Value
    - Value always > 0.1 (i.e. negative Saturation not possible)
    """
    
    # 2D saturation and value
    color2D = ee.Dictionary(ee.Dictionary(color).get('2D'))
    saturation = ee.Image(color2D.get('saturation'))
    value = ee.Image(color2D.get('value'))
    
    # saturation threshold (based on value)
    # threshold = value.subtract(0.1).updateMask(value.lte(0.2)).unmask(0.1,False)   <- original
    threshold = value.subtract(0.15).updateMask(value.lt(0.3)).unmask(0.15,False)     
  
    # cloud pixels
    grey_and_bright = saturation.lt(ee.Image(threshold))
    cold = ee.Image(BT).lt(20)
    cloud = grey_and_bright.multiply(cold)
    
    # clouds are nebulous, fluffy edges are included (100m radius)
    cloudy = cloud.distance(ee.Kernel.euclidean(100, "meters")).gte(0).unmask(0, False)
  
    return cloudy.rename(['cloud'])
    
  def water(toa):
    """
    Water pixels have an NDWI > 0.3 (Normalized Difference Water Index)
    """
    
    ndwi = ee.Image(toa).normalizedDifference(['green','nir'])
    water = ndwi.gte(0.1)
  
    return water.rename(['water'])  