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


# start Earth Engine
ee.Initialize()

target = 'Aoba'

# geometry (crater box)
geom = ee.FeatureCollection('ft:12PQq9qXwrGs_GOwaL8XtNvYEPnbhW7ercpiIFv0h')\
  .filter(ee.Filter.equals('name', target))\
  .geometry()

# ASTER scenes with VNIR and TIR (critical for color. temperature. size and cloud detection)
aster = ee.ImageCollection('ASTER/AST_L1T_003')\
  .filterBounds(geom)\
  .filterDate('1900-01-01','2016-01-01')\
  .filter(ee.Filter.And(\
    ee.Filter.listContains('ORIGINAL_BANDS_PRESENT', 'B01'),\
    ee.Filter.listContains('ORIGINAL_BANDS_PRESENT', 'B10')\
    ))
  
img = ee.Image(aster.first())
rad = Aster.radiance.fromDN(img)
ref = Aster.reflectance.fromRad(rad)
temp = Aster.temperature.fromRad(rad)

print('count = ',aster.aggregate_count('system:index').getInfo())
states = rad.get('subsystem_states')
print(states.getInfo())

