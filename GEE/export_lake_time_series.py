import ee

# load your packages
import preprocess
from atmospheric import get_water_vapour
from atmospheric import get_ozone
from lake_analysis import lake_analysis
from thermal_analysis import thermal_analysis
from doy_from_date import doy_from_date
from LEDAPS import get_LEDAPS



# extract time series data (i.e. will be mapped onto image collection)
def lake_data(img):
    
  # date
  date = ee.Date(img.get('system:time_start'))
  
  # day of year (for convenience, e.g. elliptical orbit correction)
  doy = doy_from_date(date)
  
  # preprocessing (at-sensor radiance and top-of-atmosphere reflectance)
  rad = preprocess.toRad(img)
  toa = preprocess.toToa(img)
    
  # lake analysis (mean radiances and pixel counts)
  lake = lake_analysis(rad,toa,geom)
  
  # thermal infrared analysis
  thermal = thermal_analysis(rad, toa, geom)
  
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
    'doy':doy,\
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
  
# target
# target = 'Pinatubo'
  
target_list = '/home/sam/Dropbox/HIGP/Crater_Lakes/Volcanoes/volcano_names.txt'
targets = [line.rstrip('\n') for line in open(target_list)]

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
  sats = ['L4','L5','L7','L8']
  
  for sat in sats:
    
    #image collection
    ic = ics[sat]
    
    # lake data
    data = ic.map(lake_data)
    
    # export to table
    ee.batch.Export.table.toDrive(data, sat+'_'+target,'Ldata_'+target).start()
  
  









