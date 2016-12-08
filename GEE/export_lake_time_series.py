"""
export_lake_time_series.py, Sam Murphy (2016-10-26)

Google Earth Engine task manager, sends output to Google Drive. 
output = time series volcanic craters lakes data:
- radiance (visible, nir, swir and tir)
- lake pixel count
- thermal infrared brightness temperature
- water vapour and ozone
- LEDAPS surface reflectance (where available)

output folder called 'Ldata_{target}'

"""

import ee

# load your packages
import preprocess
from atmospheric import get_water_vapour
from atmospheric import get_ozone
from lake_analysis import lake_analysis
from thermal_analysis import thermal_analysis
from doy_from_date import doy_from_date
from LEDAPS import get_LEDAPS




def color_metrics(toa):
  RGB = toa.select(['red','green','blue'])
  HSV = RGB.rgbToHsv() 
  return ee.Dictionary({'RGB': RGB,'HSV': HSV})
  
def find_water(toa):
  return toa.normalizedDifference(['green','nir']).gte(0.4).rename(['water'])
    
def find_cloud(color,BT):
  HSV = ee.Image(color.get('HSV'))
  grey = HSV.select(['saturation']).lt(0.3)
  bright = HSV.select(['value']).gt(0.1)
  cold = BT.lt(20)
  cloud = grey.multiply(bright).multiply(cold)
  cloudy = cloud.distance(ee.Kernel.euclidean(5, "pixels")).gte(0).unmask(0, False)# buffered clouds
  return cloudy.rename(['cloud'])

# extracts lake data from an image (will be mapped over image collection)
def lake_data(img):
    
  # date
  date = ee.Date(img.get('system:time_start'))
  
  # preprocessing (at-sensor radiance and top-of-atmosphere reflectance)
  rad = preprocess.toRad(img)
  toa = preprocess.toToa(img)
  
  # color metrics
  color = color_metrics(toa)
  
  # brightness temperature
  BT = toa.select('tir1').subtract(273).rename(['BT'])
  
  # water and cloud pixels
  water = find_water(toa)
  cloud = find_cloud(color,BT)  
    
  # lake analysis (mean radiances and pixel counts)
  lake = lake_analysis(geom,rad,water,cloud)
  
  # thermal infrared analysis
  thermal = thermal_analysis(geom,rad,toa,water,cloud)
  
  # solar zenith
  solar_z = ee.Number(90.0).subtract(img.get('SUN_ELEVATION'))
  
  # water vapour
  H2O = get_water_vapour(geom,date)
  
  # ozone
  O3 = get_ozone(geom,date)
  
  # LEDAPS surface reflectance (for comparison only)
  LEDAPS = ee.Dictionary(get_LEDAPS(img,date,geom))
  
  #result
  data = ee.Feature(geom,{\
    'date':date,\
    'doy':doy_from_date(date),\
    'lake_mean_rad':lake.get('lake_mean_rad'),\
    'lake_count':lake.get('lake_count'),\
    'cloud_count':lake.get('cloud_count'),\
    'valid_count':lake.get('valid_count'),\
    'solar_z':solar_z,\
    'H2O':H2O,\
    'O3':O3,\
    'LEDAPS':LEDAPS,\
    'thermal':thermal
    })    
  
  return data

#------------------------------------------------------------------------------

# start Earth Engine
ee.Initialize()

target_list = '/home/sam/Dropbox/HIGP/Crater_Lakes/Volcanoes/volcano_names.txt'
targets = [line.rstrip('\n') for line in open(target_list)]

targets = ['Aoba']

for target in targets:
  
  print(target)
  # geometry (crater box)
  geom = ee.FeatureCollection('ft:12PQq9qXwrGs_GOwaL8XtNvYEPnbhW7ercpiIFv0h')\
    .filter(ee.Filter.equals('name', target))\
    .geometry();
  
  # image collections
  ics = ({\
    'L4':ee.ImageCollection('LANDSAT/LT4_L1T').filterBounds(geom).filterDate('1900-01-01','2016-01-01'),\
    'L5':ee.ImageCollection('LANDSAT/LT5_L1T').filterBounds(geom).filterDate('1900-01-01','2016-01-01'),\
    'L7':ee.ImageCollection('LANDSAT/LE7_L1T').filterBounds(geom).filterDate('1900-01-01','2016-01-01'),\
    'L8':ee.ImageCollection('LANDSAT/LC8_L1T').filterBounds(geom).filterDate('1900-01-01','2016-01-01')
  })
  
  # satellite missions
  sats = ['L4']#,'L5','L7','L8']
  
  for sat in sats:
    
    #image collection
    ic = ics[sat]
    
    # lake data
    data = ic.map(lake_data)
    
    # export to table
    ee.batch.Export.table.toDrive(data, sat+'_'+target,'Ldata_'+target).start()










