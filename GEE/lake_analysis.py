import ee

def lake_analysis(toa,rad,geom):
  
  # water mask (i.e. keep water pixels)
  water_mask = toa.normalizedDifference(['green','nir']).gte(0.4).rename(['water_mask'])
  
  # radiance from water pixels
  water_rad = rad.updateMask(water_mask)
  
  # mean radiance from lake water
  lake_mean_rad = water_rad.reduceRegion(reducer = ee.Reducer.mean(), \
    geometry = geom, scale = 30)
  
  # count lake water pixels
  lake_pixel_count = water_mask.reduceRegion(reducer = ee.Reducer.sum(), \
    geometry = geom, scale = 30).get('water_mask').getInfo()
    
  # cloud pixels 
  cloud_pixels = toa.select(['nir']).gt(0.1).rename(['cloud'])  
    
  # count cloud pixels in target area
  cloud_count = cloud_pixels.reduceRegion(reducer = ee.Reducer.sum(), \
    geometry = geom, scale = 30).get('cloud').getInfo()
 
  return ee.Dictionary({ \
  'mask': water_mask,\
  'water_rad': water_rad,\
  'lake_mean_rad': lake_mean_rad,\
  'lake_pixel_count': lake_pixel_count,\
  'cloud_count':cloud_count \
  })