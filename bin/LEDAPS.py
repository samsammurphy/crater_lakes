"""
get_LEDAPS.py, Sam Murphy

Finds LEDAPS image for given date and geom. Returns a reduceRegion of the image
(if it exists) with
- lake (i.e. target) surface reflectance
- water, snow, shadow and cloud pixel counts

"""

import ee
import preprocess as pre

def get_LEDAPS(img,date,geom):
  
  def LEDAPS_image_found():
    
    # LEDAPS_img reflectance wavebands
    SR = LEDAPS_img.select(pre.get_vswirNums(satID),pre.get_vswirNames(satID))
    SR = ee.Image(SR).divide(ee.Number(10000).float()) #convert to Py6S units (i.e. 0-1)
  
    # cfmask
    cfmask = LEDAPS_img.select(['cfmask'])
    water  = cfmask.eq(1).rename(['water'])  
    shadow = cfmask.eq(2).rename(['shadow'])  
    snow   = cfmask.eq(3).rename(['snow'])  
    cloud  = cfmask.eq(4).rename(['cloud'])  
    
    # water pixels only
    masked = SR.updateMask(water)\
    .updateMask(cloud.eq(0))\
    .updateMask(shadow.eq(0))\
    .updateMask(snow.eq(0))    
  
    # mean reflectance of lake water pixels
    lake_SR = masked.reduceRegion(reducer = ee.Reducer.mean(),geometry = geom, scale = 30)
    
    # count pixels
    water_count  = water.reduceRegion(reducer = ee.Reducer.sum(), geometry = geom, scale = 30).get('water')
    shadow_count = shadow.reduceRegion(reducer = ee.Reducer.sum(), geometry = geom, scale = 30).get('shadow')
    snow_count   = snow.reduceRegion(reducer = ee.Reducer.sum(), geometry = geom, scale = 30).get('snow')
    cloud_count  = cloud.reduceRegion(reducer = ee.Reducer.sum(), geometry = geom, scale = 30).get('cloud')
  
    result = ee.Dictionary ({
    'lake_SR':lake_SR,
    'water_count':water_count,
    'snow_count':snow_count,
    'shadow_count':shadow_count,
    'cloud_count':cloud_count
    })
    
    return result
    
  def LEDAPS_image_not_found():
    result = ee.Dictionary ({
    'lake_SR':'null',
    'water_count':'null',
    'snow_count':'null',
    'shadow_count':'null',
    'cloud_count':'null'
    })
    
    return result
  
  # satellite ID
  satID = ee.String(img.get('system:index')).slice(0,3)
  
  # image collection for this satellite
  collection_from_satID = ee.Dictionary({
  'LT4':ee.ImageCollection('LANDSAT/LT4_SR'),
  'LT5':ee.ImageCollection('LANDSAT/LT5_SR'),
  'LE7':ee.ImageCollection('LANDSAT/LE7_SR'),
  'LC8':ee.ImageCollection('LANDSAT/LC8_SR')
  })
  
  # filter collection to this time and place
  ic = ee.ImageCollection(collection_from_satID.get(satID)).filterBounds(geom).filterDate(date)
  LEDAPS_img = ee.Image(ic.first())
  
  # if image found do processing
  result = ee.Algorithms.If(LEDAPS_img,LEDAPS_image_found(),LEDAPS_image_not_found())
  
  return result