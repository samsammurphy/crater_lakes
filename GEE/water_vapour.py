# -*- coding: utf-8 -*-
"""
# Atmospheric water vapor column (kg/m2) at given point in spacetime

"""

import ee

# H2O datetime is hour closest to 0000, 0600, 1200, or 1800 UTC
def get_H2O_datetime(img_datetime):
  y = img_datetime.get('year')
  m = img_datetime.get('month')
  d = img_datetime.get('day')
  H = img_datetime.get('hour')
  HH = H.divide(6).round().multiply(6)

  return ee.Date.fromYMD(y,m,d).advance(HH,'hour')

def get_H2O(geom,img_datetime):

  # closest H2O datetime
  H2O_datetime = get_H2O_datetime(img_datetime)
  
  #filtered water collection
  water_ic = ee.ImageCollection('NCEP_RE/surface_wv') \
    .filterBounds(geom) \
    .filterDate(H2O_datetime)
  
  #water image
  water_img = ee.Image(water_ic.first())
  
  #geolreference information
  crs = water_img.projection().crs().getInfo() 
  scale = water_img.projection().nominalScale().getInfo() 

  #water_vapour at target
  water = water_img.reduceRegion(reducer = ee.Reducer.mean(), geometry = geom, 
                                      crs = crs, scale = scale).get('pr_wtr')
                                      
  #convert to Py6S units (Google = kg/m^2, Py6S = g/cm^2)
  water_Py6S_units = ee.Number(water).divide(10).getInfo()                                   
  
  return water_Py6S_units

