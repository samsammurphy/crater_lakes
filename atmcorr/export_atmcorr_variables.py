"""
Exports the atmospheric variables for 6S

"""

import ee
import sys
sys.path.append('/home/sam/git/crater_lakes/bin')
from atmospheric import Atmospheric

ee.Initialize()

"""
Mapping function to extract variables
"""
def enclose_geom(geom):
  """
  allow the extractor() function to access the geom variable
  """
  
  def extractor(img):
    """
    extract atmospheric variables for 6S
    """
    
    date = ee.Date(img.get('system:time_start'))
    
    atmvars = ee.Dictionary({
        'solar_z':ee.Number(90.0).subtract(img.get('SUN_ELEVATION')),
        'H2O':Atmospheric.water(geom,date),
        'O3':Atmospheric.ozone(geom,date),
        'AOT':Atmospheric.aerosol(geom,date),
        'datetime':date,
        'satID':ee.String(img.get('system:index')).slice(0,3)
        })

    return ee.Feature(geom,atmvars)
  
  return extractor


# target name and location
target = 'Kelimutu'
geom = ee.Geometry.Point(121.8137, -8.767)

# atmospheric variables
get_atmvars = enclose_geom(geom.centroid())# create enclosure of mapping function
L4 = ee.ImageCollection('LANDSAT/LT4_L1T').filterBounds(geom).map(get_atmvars)
L5 = ee.ImageCollection('LANDSAT/LT5_L1T').filterBounds(geom).map(get_atmvars)
L7 = ee.ImageCollection('LANDSAT/LE7_L1T').filterBounds(geom).map(get_atmvars)
L8 = ee.ImageCollection('LANDSAT/LC8_L1T').filterBounds(geom).map(get_atmvars)
atmvars = ee.FeatureCollection([L4,L5,L7,L8]).flatten()

# export
ee.batch.Export.table.toDrive(collection = atmvars,\
                            description = 'atmospheric_variables_export',\
                            folder = 'LakeData_'+target,\
                            fileNamePrefix = 'atmospheric_variables'\
                            ).start()



