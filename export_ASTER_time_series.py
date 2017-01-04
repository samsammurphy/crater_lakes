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
  
  #2D color: ASTER + LANDSAT
  R = ee.Image(toa).select(['red'])
  G = ee.Image(toa).select(['green'])
  saturation = G.subtract(R)#.rename('saturation')
  value = ee.Image(R.max(G)).rename('value')
  metrics = ee.Dictionary({'2D':{'saturation':saturation,'value':value}})  
  
  # 3D color: LANDSAT only
  def add_HSV(metrics):
    RGB = ee.Image(toa).select(['red','green','blue'])
    HSV = RGB.rgbToHsv() 
    metrics['3D'] = HSV
    return metrics
    
  metrics = ee.Algorithms.If('SATID = AST',metrics,add_HSV(metrics))
    
  return metrics

def cloud_mask():
  cloud = 'latest algorithm'
  return cloud  
  
def water_mask():
  water = 'latest algorithm'
  return water  
  
  
  
# extracts lake data from an image (will be mapped over image collection)
def lake_data(img, geom):
  
  # preprocessing
  rad = Aster.radiance.fromDN(img)     # at-sensor radiance
  toa = Aster.reflectance.fromRad(rad) # top of atmosphere reflectance
#  BT = Aster.temperature.fromRad(rad)  # brightness temperature
   
  # color metrics
  color = color_metrics(toa.get('vnir'),color2D=True)
  
  return color
  
#  # water and cloud pixels
#  water = find_water(toa)
#  cloud = find_cloud(color,BT)  
#  
#  # lake analysis (mean radiances and pixel counts)
#  lake = lake_analysis(geom,rad,water,cloud)
#  
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
