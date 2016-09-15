import ee

# load your packages
import preprocess
from atmospheric import get_water_vapour
from atmospheric import get_ozone
from lake_analysis import lake_analysis
from doy_from_date import doy_from_date

# start Earth Engine
ee.Initialize()

# extract time series data (i.e. will be mapped onto image collection)
def lake_data(img):
  
  # date
  date = ee.Date(img.get('system:time_start'))
  
  # day of year (for convenience, e.g. elliptical orbit correction)
  doy = doy_from_date(date)
  
  # preprocessing (at-sensor radiance and top-of-atmosphere reflectance)
  rad = preprocess.toRad(img)
  toa = preprocess.toToa(img)
  
  # radiance from lake
  lake = lake_analysis(toa,rad,geom)
  lake_pixel_count = lake.get('lake_pixel_count')
  lake_mean_rad = lake.get('lake_mean_rad')
  cloud_count = lake.get('cloud_count')

  # solar zenith
  solar_e = ee.Number(img.get('SUN_ELEVATION')).float()
  solar_z = ee.Number(90.0).subtract(solar_e)
  
  # water vapour
  H2O = get_water_vapour(geom.centroid(),date)
  
  #ozone
  O3 = get_ozone(geom.centroid(),date,ozone_fill)

  #result
  data = ee.Feature(geom,{\
    'date':date,\
    'doy':doy,\
    'lake_pixel_count':lake_pixel_count,\
    'lake_mean_rad':lake_mean_rad,\
    'solar_z':solar_z,\
    'H2O':H2O,\
    'O3':O3,\
    'cloud_count':cloud_count
    })    
  
  return data

# target location
target = 'Aoba'

geom = ee.Geometry.Polygon([[167.82157, -15.38674],[167.82938, -15.38294],\
  [167.83908, -15.386],[167.84174, -15.39237],[167.840195, -15.395349],\
  [167.82706, -15.39767],[167.82389, -15.39659],[167.82045, -15.38972]])

# my ozone fill values (i.e. for TOMS hiatus and other data gaps)
ozone_fill = ee.ImageCollection('users/samsammurphy/public/ozone_fill').toList(366)

# image collections
ics = ({\
  'L4':ee.ImageCollection('LANDSAT/LT4_L1T').filterBounds(geom),\
  'L5':ee.ImageCollection('LANDSAT/LT5_L1T').filterBounds(geom),\
  'L7':ee.ImageCollection('LANDSAT/LE7_L1T').filterBounds(geom),\
  'L8':ee.ImageCollection('LANDSAT/LC8_L1T').filterBounds(geom).filterDate('1900-01-01','2016-01-01')
})

# satellite missions
sats = ['L4','L5','L7','L8']

for sat in sats:
  ic = ics[sat]
  
  # result
  data = ic.map(lake_data)
  
  # export to table
  ee.batch.Export.table.toDrive(data, sat+'_'+target,'Ldata_'+target).start()



 












