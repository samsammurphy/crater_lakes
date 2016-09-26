import ee

def thermal_analysis(rad,toa,geom):
  
  # TIR radiance
  TIR = rad.select(['tir1']).rename(['TIR'])
  
  # brightness temperature
  BT = toa.select('tir1').subtract(273).rename(['BT'])
   
  # HSV color transform (cloud and snow mask)
  RGB = toa.select(['red','green','blue'])
  HSV = RGB.rgbToHsv()
  
  # clouds (and snow/ice)
  grey = HSV.select(['saturation']).lt(0.3)
  bright = HSV.select(['value']).gt(0.1)
  cold = BT.lt(20)
  cloud_pixels = grey.multiply(bright).multiply(cold)
  cloudy = cloud_pixels.distance(ee.Kernel.euclidean(5, "pixels")).gte(0).unmask(0, False)# buffered clouds
  
  # water 
  water_pixels = toa.normalizedDifference(['green','nir']).gte(0.4).rename(['water'])
  watery = water_pixels.distance(ee.Kernel.euclidean(4, "pixels")).gte(0).unmask(0, False)# buffered water
  
  # lake pixels
  lake_BT = BT.updateMask(water_pixels).rename(['lake_BT'])
  lake_TIR = TIR.updateMask(water_pixels).rename(['lake_TIR'])
  lake = lake_BT.addBands(lake_TIR)
  
  # background (land) pixels
  bkgd_BT = BT.updateMask(watery.eq(0)).updateMask(cloudy.eq(0)).rename(['bkgd_BT'])
  bkgd_TIR = TIR.updateMask(watery.eq(0)).updateMask(cloudy.eq(0)).rename(['bkgd_TIR'])
  bkgd = bkgd_BT.addBands(bkgd_TIR)
  
  # lake stats
  lake_stats = lake.reduceRegion(reducer = ee.Reducer.mean(), \
    geometry = geom, scale = TIR.projection().nominalScale())
    
  # background (land) stats
  bkgdArea = geom.buffer(600).difference(geom.buffer(150))
  bkgd_stats = bkgd.reduceRegion(reducer = ee.Reducer.mean(), \
    geometry = bkgdArea, scale = TIR.projection().nominalScale())

  return ee.Dictionary({ \
  'lake_BT': lake_stats.get('lake_BT'),\
  'lake_TIR': lake_stats.get('lake_TIR'),\
  'bkgd_BT': bkgd_stats.get('bkgd_BT'),\
  'bkgd_TIR': bkgd_stats.get('bkgd_TIR') \
  })