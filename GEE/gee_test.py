# The package is in the site-packages directory:
# /home/sam/anaconda3/lib/python3.5/site-packages/gee

# start Earth Engine
import ee
ee.Initialize()

# load your package
import preprocess
from atmospheric import get_water_vapour
from lake_analysis import lake_analysis
from doy_from_eeDate import doy_from_eeDate
from AOT import get_AOT
from iLUTs import load_iLUTs
from set_scene_info import set_scene_info
from surface_reflectance import surface_reflectance as SR

# GEE
# --------------------------------------------------------------------------
# target location
geom = ee.Geometry.Polygon([[167.82157, -15.38674],[167.82938, -15.38294],\
  [167.83908, -15.386],[167.84174, -15.39237],[167.840195, -15.395349],\
  [167.82706, -15.39767],[167.82389, -15.39659],[167.82045, -15.38972]])

# satellite imagery
img = ee.Image('LANDSAT/LC8_L1T/LC80820702015042LGN00')
rad = preprocess.toRad(img)
toa = preprocess.toToa(img)

# satellite ID
satID = img.get('SPACECRAFT_ID').getInfo()

# radiance from lake
lake = lake_analysis(toa,rad,geom)
lake_pixels = lake.get('lake_pixel_count').getInfo()
lake_mean_rad = lake.get('lake_mean_rad').getInfo()

# lake detected?
if lake_pixels == 0:
  print('no water pixels found')
else:

  # datetime
  eeDate = ee.Date(img.get('system:time_start'))
  
  # solar zenith
  solar_e = img.get('SUN_ELEVATION').getInfo()
  solar_z = 90-float(solar_e)
  
  # water vapour and ozone
  H2O = get_water_vapour(geom.centroid(),eeDate).getInfo()
  print('water vapour = ',H2O)
  O3 = 0.4
  
  # day of year
  doy = doy_from_eeDate(eeDate).getInfo()
  
  
# Python 
# --------------------------------------------------------------------------
# target specific information 
target = 'Aoba'
aerosol = 'MA'

# interpolated look-up tables for this aerosol
all_iLUTs = load_iLUTs(aerosol)

# scene specific information
scene_info = set_scene_info(target,satID,solar_z,H2O,O3,doy)

# Look-up tables to use for this scene (i.e. one for each waveband)
iLUTs = all_iLUTs[scene_info['sensor']]

# AOT estimate
scene_info['AOT'] = get_AOT(lake_mean_rad, iLUTs, scene_info)

# surface reflectance
ref = {}
for band_name in scene_info['band_names']:
  ref[band_name] = SR(lake_mean_rad[band_name], iLUTs[band_name], scene_info)

print(ref)









