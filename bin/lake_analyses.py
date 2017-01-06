"""
lake_analysis.py, Sam Murphy (2016-10-24)

VSWIR analysis of crater radiance and top-of-atmosphere reflectance.

- lake_mean_radiance
- lake pixel count
- 'cloud' count
- valid pixel count (i.e. not null)

"""

import ee

def vnir_analysis(rad,geom,cloud,water):
    
  # vnir radiance
  vnir = ee.Image(ee.Dictionary(rad).get('vnir'))
    
  # water radiance
  water_rad = vnir.updateMask(water)
  
  # spatial resolution of pixels
  scale = ee.Number(vnir.projection().nominalScale())
  
  # mean radiance from lake
  mean_rad = water_rad.reduceRegion(ee.Reducer.mean(), geom, scale)
  
  return 1
  
#  # lake pixel count
#  lake_count = water.reduceRegion(reducer = ee.Reducer.sum(), \
#    geometry = geom, scale = scale).get('nd')
#        
#  # cloud pixel count
#  cloud_count = cloud.reduceRegion(reducer = ee.Reducer.sum(), \
#    geometry = geom, scale = scale)#.get('cloud')
#    
#  # valid pixel count
#  valid_count = vnir.reduceRegion(reducer = ee.Reducer.count(), \
#    geometry = geom, scale = scale)
#  
#  return ee.Dictionary({ \
#  'mean_radiance': lake_mean_rad,\
#  'pixel_counts': ee.Dictionary({
#    'lake':lake_count,
#    'cloud':cloud_count,
#    'valid':valid_count})\
#  })
