"""
lake_analysis.py, Sam Murphy (2016-10-24)

VSWIR analysis of crater radiance and top-of-atmosphere reflectance.

- lake_mean_radiance
- lake pixel count
- 'cloud' count      <-- needs updating
- valid pixel count (i.e. not null)

"""

import ee

def lake_analysis(geom,rad,water,cloud):
  
  #TODO! 
  # - dynamic scale (i.e. 15, 30, etc.)
  # - check TIR band is valid too! (think you might be saving here but using later?)
  # - check water and cloud are latest masks
   
  # radiance from water pixels
  water_rad = rad.updateMask(water)
  
  # mean radiance from lake water
  lake_mean_rad = water_rad.reduceRegion(reducer = ee.Reducer.mean(), \
    geometry = geom, scale = 30)
  
  # lake pixel count
  lake_count = water.reduceRegion(reducer = ee.Reducer.sum(), \
    geometry = geom, scale = 30).get('water')
        
  # cloud pixel count
  cloud_count = cloud.reduceRegion(reducer = ee.Reducer.sum(), \
    geometry = geom, scale = 30).get('cloud')
    
  # valid pixel count
  valid_count = rad.reduceRegion(reducer = ee.Reducer.count(), \
    geometry = geom, scale = 30)
  
  return ee.Dictionary({ \
  'water_rad': water_rad,\
  'lake_mean_rad': lake_mean_rad,\
  'lake_count': lake_count,\
  'cloud_count':cloud_count, \
  'valid_count':valid_count \
  })