import ee

def lake_analysis(rad,toa,geom):
  
  # water pixels
  water_pixels = toa.normalizedDifference(['green','nir']).gte(0.4).rename(['water'])
  
  # cloud pixels 
  cloud_pixels = toa.select(['nir']).gt(0.1).rename(['cloud'])  
  
  # radiance from water pixels
  water_rad = rad.updateMask(water_pixels)
  
  # mean radiance from lake water
  lake_mean_rad = water_rad.reduceRegion(reducer = ee.Reducer.mean(), \
    geometry = geom, scale = 30)
  
  # lake pixel count
  lake_count = water_pixels.reduceRegion(reducer = ee.Reducer.sum(), \
    geometry = geom, scale = 30).get('water')
        
  # cloud pixel count
  cloud_count = cloud_pixels.reduceRegion(reducer = ee.Reducer.sum(), \
    geometry = geom, scale = 30).get('cloud')
    
  # valid pixel count
  valid_count = rad.reduceRegion(reducer = ee.Reducer.count(), \
    geometry = geom, scale = 30)
  
  return ee.Dictionary({ \
  'water': water_pixels,\
  'water_rad': water_rad,\
  'lake_mean_rad': lake_mean_rad,\
  'lake_count': lake_count,\
  'cloud_count':cloud_count, \
  'valid_count':valid_count \
  })