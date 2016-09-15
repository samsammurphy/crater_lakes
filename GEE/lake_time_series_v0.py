# Extracts data and metadata from lakes through time
# ! uses a for loop and getInfo (emergency back-up)
# plan is to map the function and get GEE to deliver results as a feature collection

import ee
import sys
import time

# load your package
import preprocess
from atmospheric import get_water_vapour
from atmospheric import get_ozone
from lake_analysis import lake_analysis
from AOT import get_AOT
from iLUTs import load_iLUTs
from set_scene_info import set_scene_info
from surface_reflectance import surface_reflectance as SR
from doy_from_eeDate import doy_from_eeDate

# GEE
# --------------------------------------------------------------------------
# start Earth Engine
ee.Initialize()

# target location
geom = ee.Geometry.Polygon([[167.82157, -15.38674],[167.82938, -15.38294],\
  [167.83908, -15.386],[167.84174, -15.39237],[167.840195, -15.395349],\
  [167.82706, -15.39767],[167.82389, -15.39659],[167.82045, -15.38972]])

# imagery
ic = ee.ImageCollection('LANDSAT/LC8_L1T').filterBounds(geom)
ic_list = ic.toList(200)

t = time.time()
for i in range(0,10):
  
  print(i)
  img = ee.Image(ic_list.get(i))
  
  # preprocessing (at-sensor radiance and top-of-atmosphere reflectance)
  rad = preprocess.toRad(img)
  toa = preprocess.toToa(img)
  
  # radiance from lake
  lake = lake_analysis(toa,rad,geom)
  lake_pixels = lake.get('lake_pixel_count').getInfo()
  lake_mean_rad = lake.get('lake_mean_rad').getInfo()
  
  # lake detected?
  if lake_pixels == 0:
    print('no water pixels found')
  else:
  
    # datetime
    date = ee.Date(img.get('system:time_start'))
    
    # solar zenith
    solar_e = img.get('SUN_ELEVATION').getInfo()
    solar_z = 90-float(solar_e)
    print('solar_z = ',solar_z)
    
    # water vapour
    H2O = get_water_vapour(geom.centroid(),date).getInfo()
    print('water vapour = ',H2O)
    
    #ozone
    ozone_fill = ee.ImageCollection('users/samsammurphy/public/ozone_fill').toList(366)
    O3 = get_ozone(geom.centroid(),date,ozone_fill).getInfo()
    print('ozone = ',O3)
    
    #satellite ID (from preprocess)
    satID = img.get('SPACECRAFT_ID').getInfo()
    print('satID = ',satID)
    
    # day of year (elliptical orbit correction)
    doy = doy_from_eeDate(date).getInfo()
    print('doy = ',doy)
 
print(time.time()-t)
## Python 
## --------------------------------------------------------------------------
## target specific information 
#target = 'Aoba'
#aerosol = 'MA'
#
## interpolated look-up tables for this aerosol
#all_iLUTs = load_iLUTs(aerosol)
#
## scene specific information
#scene_info = set_scene_info(target,satID,solar_z,H2O,O3,doy)
#
## Look-up tables to use for this scene (i.e. one for each waveband)
#iLUTs = all_iLUTs[scene_info['sensor']]
#
## AOT estimate
#scene_info['AOT'] = get_AOT(lake_mean_rad, iLUTs, scene_info)
#
## surface reflectance
#ref = {}
#for band_name in scene_info['band_names']:
#  ref[band_name] = SR(lake_mean_rad[band_name], iLUTs[band_name], scene_info)
#
#print(ref)









