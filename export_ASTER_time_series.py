"""
export_ASTER_time_series.py, Sam Murphy (2017-01-02)

This is a Google Earth Engine task manager. It sends lake data to a 
Google Drive folder called 'Ldata_{target}'

OUTPUT
-------------------------------------------------------------------------------
- radiance (visible, nir, swir and tir)
- lake pixel count
- thermal infrared brightness temperature
- water vapour and ozone

NOTE
-------------------------------------------------------------------------------
ASTER processing is separated from Landsat due to differences in operational
functionality of these missions. ASTER has separate subsystems which can be
on/off and have dynamic gain coefficients.
"""

import ee
from preprocess_ASTER import Aster
from atmospheric import get_water_vapour
from atmospheric import get_ozone
from lake_analyses import vnir_analysis
from doy_from_date import doy_from_date




def color_metrics(toa):
  """
  Calculates 
  
  - (new) 2D 'saturation' and 'value' of red-green space
  - (traditional) 3D Hue-Saturation-Value IF blue band available.
  
  """
  
  # 2D color: ASTER & LANDSAT
  R = ee.Image(toa).select(['red'])
  G = ee.Image(toa).select(['green'])
  saturation = R.subtract(G).abs()
  value = R.max(G)
  metrics = ee.Dictionary({'2D':
                              ee.Dictionary({'saturation':saturation,'value':value})
                          })
  
  # 3D color
  hasBlue = ee.List(ee.Image(toa).bandNames()).contains('blue')
  HSV = ee.Algorithms.If(hasBlue,\
    ee.Image(toa).select(['red','green','blue']).rgbToHsv(),'null')
  metrics = ee.Dictionary(metrics).set('3D',HSV)
      
  return metrics

def cloud_mask(color, BT):
  """
  Cloud pixels are grey, bright and cold
  
  - grey and bright: 2D Saturation and Value
  - cold: Brightness Temperature
  
  More detail on grey and bright threshold:
  - Saturation always < 0.1
  - if Value between 0.1 and 0.2 then Saturation must be 0.1 less than Value
  - Value always > 0.1 (i.e. negative Saturation not possible)
  """
  
  # 2D saturation and value
  color2D = ee.Dictionary(ee.Dictionary(color).get('2D'))
  saturation = ee.Image(color2D.get('saturation'))
  value = ee.Image(color2D.get('value'))
  
  # saturation threshold (based on value)
  threshold = value.subtract(0.1).updateMask(value.lte(0.2)).unmask(0.1,False)    

  # cloud pixels
  grey_and_bright = saturation.lt(ee.Image(threshold))
  cold = ee.Image(BT).lt(20)
  cloud = grey_and_bright.multiply(cold)
  
  # clouds are nebulous, fluffy edges are included (up to 5 pixels away)
  cloudy = cloud.distance(ee.Kernel.euclidean(5, "pixels")).gte(0).unmask(0, False)

  return cloudy
  
def water_mask(toa):
  """
  Water pixels have an NDWI > 0.3 (Normalized Difference Water Index)
  """
  
  ndwi = ee.Image(toa).normalizedDifference(['green','nir'])
  water = ndwi.gte(0.0)
  # Note! originally 0.3 (i.e. for Landsat)
  # however, set to zero because ASTER nir is less effective at water detection
  # due to slightly shorter wavelength. 
  # You should be able to get away with this..
  # IF YOU DRAW A CRATER OUTLINE FOR EACH TARGET VOLCANO!!

  return water  
  
  
  
# lake data from single image (will be mapped over image collection)
def lake_data(img, geom):
  
  # preprocessing
  rad = Aster.radiance.fromDN(img)     # at-sensor radiance
  toa = Aster.reflectance.fromRad(rad) # top of atmosphere reflectance
  BT  = Aster.temperature.fromRad(rad) # brightness temperature
   
  # color metrics
  color = color_metrics(toa.get('vnir'))

  # cloud mask
  cloud = cloud_mask(color, BT)
  
  # water mask
  water = water_mask(toa.get('vnir')) 
  
  
  toa = ee.Image(ee.Dictionary(toa).get('vnir'))
  img = ee.Image(toa).normalizedDifference(['green','nir'])
  scale = ee.Number(img.projection().nominalScale())
  lake_mean = img.reduceRegion(ee.Reducer.mean(), geom, scale)
  print(lake_mean.getInfo())
  

  
  # lake analyses (mean radiances and pixel counts)
  #vnir_results = vnir_analysis(rad,geom,cloud,water)
  #swir_results = swir_analysis(rad,geom,cloud,water)
  
#  # thermal infrared analysis
#  thermal = thermal_analysis(geom,rad,toa,water,cloud)
#  
#  date = ee.Date(img.get('system:time_start'))
#
#
#    #result
#  return ee.Feature(geom,{\
#    'date':date,\
#    'doy':doy_from_date(date),\
##    'lake_mean_rad':lake.get('lake_mean_rad'),\
##    'lake_count':lake.get('lake_count'),\
##    'cloud_count':lake.get('cloud_count'),\
##    'valid_count':lake.get('valid_count'),\
#    'solar_z':ee.Number(90.0).subtract(img.get('SOLAR_ELEVATION')),\
#    'H2O':get_water_vapour(geom,date),\
#    'O3':get_ozone(geom,date),\
##    'thermal':thermal
#    })    

  return 1#vnir_results


def main():
  
  # start Earth Engine
  ee.Initialize()
  
  target = 'Aso'
  
  # geometry (crater box)
  geom = ee.FeatureCollection('ft:1hReJyYMkes0MO2Kgl6zTsKPjruTimSfRSWqQ1dgF')\
    .filter(ee.Filter.equals('name', target))\
    .geometry()
  
  # image collection
  aster = ee.ImageCollection('ASTER/AST_L1T_003')\
    .filterBounds(geom)\
    .filterDate('1900-01-01','2016-01-01')\
    .filter(ee.Filter.And(\
      ee.Filter.listContains('ORIGINAL_BANDS_PRESENT', 'B01'),\
      ee.Filter.listContains('ORIGINAL_BANDS_PRESENT', 'B10')\
      ))
      # filter ensures VNIR and TIR subsystems are ON.
  #print('count = ',aster.aggregate_count('system:index').getInfo())
  
  # feature collection of results
  img = ee.Image(aster.first())
  test = lake_data(img,geom)

if __name__ == '__main__':
  main()
