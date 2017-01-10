"""
lake_analysis.py, Sam Murphy (2016-10-24)

VSWIR analysis of crater radiance and top-of-atmosphere reflectance.

- lake_mean_radiance
- lake pixel count
- 'cloud' count
- valid pixel count (i.e. not null)

"""

import ee

class LakeAnalysis():
  
  def vnir(rad,geom,cloud,water):
    """
    Calculates mean lake radiance in VNIR, also returns counts for
    clouds and valid pixels
    """
      
    # vnir radiance
    vnir = ee.Image(ee.Dictionary(rad).get('vnir'))
      
    # spatial resolution of pixels
    scale = ee.Number(vnir.projection().nominalScale())
  
    # water & not cloud
    water_rad = vnir.updateMask(water).updateMask(cloud.eq(0))
      
    # mean radiance from lake
    mean_rad = water_rad.reduceRegion(ee.Reducer.mean(), geom, scale)
    
  #  # lake pixel count
    lake_count = water.reduceRegion(reducer = ee.Reducer.sum(), \
      geometry = geom, scale = scale).get('water')
    
    # cloud pixel count
    cloud_count = cloud.reduceRegion(reducer = ee.Reducer.sum(), \
      geometry = geom, scale = scale).get('cloud')
      
    # valid pixel count
    valid_count = vnir.reduceRegion(reducer = ee.Reducer.count(), \
      geometry = geom, scale = scale)
    
    return ee.Dictionary({ \
    'mean_radiance': mean_rad,\
    'pixel_counts': ee.Dictionary({
      'lake':lake_count,
      'cloud':cloud_count,
      'valid':valid_count})\
    })
  
    
  def swir(rad,geom,cloud,water):
    """
    Calculates mean lake radiance in SWIR
    """
      
    def getSwir():# ASTER SWIR maybe OFF (VNIR and TIR always ON via filtering)
    
      # swir radiance
      swir = ee.Image(ee.Dictionary(rad).get('swir'))
      
      # reproject masks
      swir_crs = swir.projection().crs()
      swir_scale = ee.Number(swir.projection().nominalScale())  
      swir_cloud = cloud.reproject(crs=swir_crs, scale=swir_scale)
      swir_water = water.reproject(crs=swir_crs, scale=swir_scale)
      
            
      # water & not cloud
      water_rad = swir.updateMask(swir_water).updateMask(swir_cloud.eq(0))
        
      # mean radiance from lake
      mean_rad = water_rad.reduceRegion(ee.Reducer.mean(), geom, swir_scale)
          
      return mean_rad
      
    return ee.Algorithms.If(ee.Dictionary(rad).get('swir'),getSwir(),False)

    
  def tir(rad,geom,cloud,water):
    """
    Calculates mean lake radiance in TIR
    """
      
    # tir radiance
    tir = ee.Image(ee.Dictionary(rad).get('tir'))
    
    # reproject masks
    tir_crs = tir.projection().crs()
    tir_scale = ee.Number(tir.projection().nominalScale())  
    tir_cloud = cloud.reproject(crs=tir_crs, scale=tir_scale)
    tir_water = water.reproject(crs=tir_crs, scale=tir_scale)
    
    # water & not cloud
    water_rad = tir.updateMask(tir_water).updateMask(tir_cloud.eq(0))
    
    # land & not cloud
    land_rad = tir.updateMask(tir_water.eq(0)).updateMask(tir_cloud.eq(0))
    
    # background area
    bkgdArea = geom.buffer(600).difference(geom.buffer(150))
    
    # mean lake radiance
    lake_rad = water_rad.reduceRegion(reducer = ee.Reducer.mean(), \
      geometry = geom, scale = tir_scale)
    
    # mean background radiance
    bkgd_rad = land_rad.reduceRegion(reducer = ee.Reducer.mean(), \
      geometry = bkgdArea, scale = tir_scale)
        
    return ee.Dictionary({
      'lake_rad': lake_rad,
      'bkgd_rad': bkgd_rad
      })