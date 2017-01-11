"""
get_LEDAPS.py, Sam Murphy

Finds LEDAPS image for given date and geom. Returns a reduceRegion of the image
(if it exists) with
- lake (i.e. target) surface reflectance
- water, snow, shadow and cloud pixel counts

"""

import ee
import preprocess_LANDSAT


class Ledaps():
  """
  Finds LEDAPS image and returns statistics (if available)
  """
  
  def found(ledaps_img,geom,satID):
    """
    LEDAPS image found; return statistics
    """
    
    # is this a Landsat 8 image?
    isL8 = preprocess_LANDSAT.Satellite.isL8(satID)
    
    # band numbers in visible to short-wave infrared
    vswirNums = ee.Algorithms.If(isL8,\
                          ['B2','B3','B4','B5','B6','B7'],\
                          ['B1','B2','B3','B4','B5','B7'])
    
    # LEDAPS_img reflectance wavebands
    SR = ee.Image(ledaps_img.select(vswirNums,['blue','green','red','nir','swir1','swir2']))\
    .divide(ee.Number(10000).float()) #convert to Py6S units (i.e. 0-1)
  
    # cfmask
    cfmask = ledaps_img.select(['cfmask'])
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
    
  def notFound():
    """
    LEDAPS image NOT found
    
    """
    
    return ee.Dictionary ({
    'lake_SR':'null',
    'water_count':'null',
    'snow_count':'null',
    'shadow_count':'null',
    'cloud_count':'null'
    })
    
  def find(img,date,geom):
    """
    Look for LEDAPS image that corresponds to this landsat scene
    """
      
    # image collections
    collections = ee.Dictionary({
    'LT4':ee.ImageCollection('LANDSAT/LT4_SR'),
    'LT5':ee.ImageCollection('LANDSAT/LT5_SR'),
    'LE7':ee.ImageCollection('LANDSAT/LE7_SR'),
    'LC8':ee.ImageCollection('LANDSAT/LC8_SR')
    })
    
    # satellite ID
    satID = preprocess_LANDSAT.Satellite.ID(img)
    
    # collection for this satellite
    collection = ee.ImageCollection(collections.get(satID))
    
    # LEDAPS img
    ledaps_img = ee.Image(collection.filterBounds(geom).filterDate(date).first())

    return ee.Algorithms.If(ledaps_img,Ledaps.found(ledaps_img,geom,satID),Ledaps.notFound())
    