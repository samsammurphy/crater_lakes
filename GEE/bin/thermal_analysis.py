"""
Thermal infrared analysis of crater lake data, returns:
- radiance and brightness temperature of both the lake and the background

"""

import ee

def thermal_analysis(geom,rad,toa,water,cloud):
  
  # TIR radiance
  TIR = rad.select(['tir1']).rename(['TIR'])
  
  # brightness temperature
  BT = toa.select('tir1').subtract(273).rename(['BT'])
  
  # lake pixels
  lake_BT = BT.updateMask(water).rename(['lake_BT'])
  lake_TIR = TIR.updateMask(water).rename(['lake_TIR'])
  lake = lake_BT.addBands(lake_TIR)
  
  # background (land) pixels
  bkgd_BT = BT.updateMask(water.eq(0)).updateMask(cloud.eq(0)).rename(['bkgd_BT'])
  bkgd_TIR = TIR.updateMask(water.eq(0)).updateMask(cloud.eq(0)).rename(['bkgd_TIR'])
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