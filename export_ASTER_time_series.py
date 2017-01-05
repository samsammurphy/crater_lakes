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
from lake_analysis import lake_analysis
from thermal_analysis import thermal_analysis
from doy_from_date import doy_from_date




def color_metrics(toa, satID):
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
  metrics = ee.Dictionary({'2D':{'saturation':saturation,'value':value}})
  
  # 3D color
  hasBlue = ee.List(ee.Image(toa).bandNames()).contains('blue')# blue band exists?
  HSV = ee.Algorithms.If(hasBlue,\
    ee.Image(toa).select(['red','green','blue']).rgbToHsv(),'null')
  
  # add 3D color
  metrics = metrics.set('3D',HSV)
      
  return metrics

def cloud_mask(color, BT):
  """
  Cloud pixels are grey, bright and cold
  
  - grey and bright: 2D saturation and value
  - cold: brightness temperature
  
  """
  
  color2D = ee.Dictionary(ee.Dictionary(color).get('2D'))
  saturation = ee.Image(color2D.get('saturation'))
  value = ee.Image(color2D.get('value'))
  
  #saturation threshold
  threshold = value.subtract(0.1).updateMask(value.lte(0.2)).unmask(0.1,False)
  # i.e. 
  # saturation must be 0.1 lower than brightness values between 0 and 0.2
  # and always lower than 0.1 in magnitude.
  
  # cloud pixels
  grey_and_bright = saturation.lt(ee.Image(threshold))
  cold = ee.Image(BT).lt(20)
  cloud = grey_and_bright.multiply(cold)
  
  # clouds are nebulous, fluffy edges are included (up to 5 pixels away)
  cloudy = cloud.distance(ee.Kernel.euclidean(5, "pixels")).gte(0).unmask(0, False)

  return cloudy
  
def water_mask(toa):
  """
  Water pixels have an NDWI > 0.3 (where NDWI = Normalized Difference Water Index)
  """
    
  ndwi = ee.Image(toa).normalizedDifference(['green','nir'])
  water = ndwi.gte(0.3)

  return water  
  
  
  
# extracts lake data from an image (will be mapped over image collection)
def lake_data(img, geom):
  
  # preprocessing
  rad = Aster.radiance.fromDN(img)     # at-sensor radiance
  toa = Aster.reflectance.fromRad(rad) # top of atmosphere reflectance
  BT  = Aster.temperature.fromRad(rad)  # brightness temperature
   
  # color metrics
  color = color_metrics(toa.get('vnir'),'AST')
  
  # cloud mask
  cloud = cloud_mask(color, BT)
  
  # water mask
  water = water_mask(toa.get('vnir'))
  
  # lake analysis (mean radiances and pixel counts)
  lake = lake_analysis(geom,rad,cloud,water)
  
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

  return lake


def main():
  # start Earth Engine
  ee.Initialize()
  
  target = 'Aoba'
  
  # geometry (crater box)
  geom = ee.FeatureCollection('ft:12PQq9qXwrGs_GOwaL8XtNvYEPnbhW7ercpiIFv0h')\
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
  test = lake_data(ee.Image(aster.first()),geom)
  print(test.getInfo())

if __name__ == '__main__':
  main()
