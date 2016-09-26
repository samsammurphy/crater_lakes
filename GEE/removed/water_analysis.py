import ee

def water_analysis(toa,rad,geom):
  
  # water mask
  water_mask = toa.normalizedDifference(['green','nir']).gte(0.4).rename(['water_mask'])
  
  # water pixels
  water_rad = rad.updateMask(water_mask)
  
  # mean radaince from lake water
  lake_mean_rad = water_rad.reduceRegion(reducer = ee.Reducer.mean(), \
    geometry = geom, scale = 30)
  
  # count pixels
  lake_pixel_count = water_mask.reduceRegion(reducer = ee.Reducer.count(), \
    geometry = geom, scale = 30).get('water_mask')
    
  return ee.Dictionary({ \
  'mask': water_mask,\
  'water_rad': water_rad,\
  'lake_mean_rad': lake_mean_rad,\
  'lake_pixel_count': lake_pixel_count
  })