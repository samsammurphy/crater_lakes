"""
export_atmcorr_variables.py, Sam Murphy (2017-04-18)

Exports atmospheric variables required for atmospheric correction
using 6S (or a 6S emulator)

"""

import ee
import sys
sys.path.append('/home/sam/git/crater_lakes/bin')
from atmospheric import Atmospheric

ee.Initialize()

"""
Mapping function to extract variables within this enclosure
"""
def enclose_geom(geom):
  """
  encloses geom variable into mapping_function()
  """
  
  def mapping_function(img):
    """
    extracts atmospheric variables for 6S
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
  
  return mapping_function

def main():

  args = sys.argv[1:]

  if len(args) != 3:
    print('usage: $ python3 export_atmcorr_variables.py {target_name} {longitude} {latitude} \n'
    'where: \n'
    '{target_name} = string identifier of target location \n'
    '{longitude} = decimal longitude (i.e. floating point) \n'
    '{latitude} = decimal latitude (i.e. floating point)')
    return
  
  try:

    # target name and location
    target = args[0]
    lon = float(args[1])
    lat = float(args[2])

    # enclose geometry into a mapping function that will extract the atmospheric variables
    geom = ee.Geometry.Point(lon,lat)
    atmvar_extractor = enclose_geom(geom)

    # process Landsat 4-8
    L4 = ee.ImageCollection('LANDSAT/LT4_L1T').filterBounds(geom).map(atmvar_extractor)
    L5 = ee.ImageCollection('LANDSAT/LT5_L1T').filterBounds(geom).map(atmvar_extractor)
    L7 = ee.ImageCollection('LANDSAT/LE7_L1T').filterBounds(geom).map(atmvar_extractor)
    L8 = ee.ImageCollection('LANDSAT/LC8_L1T').filterBounds(geom).map(atmvar_extractor)

    # join results into single feature collection
    atmvars = ee.FeatureCollection([L4,L5,L7,L8]).flatten()

    # export
    ee.batch.Export.table.toDrive(collection = atmvars,\
                                description = 'atmospheric_variables_export',\
                                fileNamePrefix = 'atmospheric_variables_'+target
                                ).start()
  except:
    print('There was an error exporting the atmospheric variables')

if __name__ == '__main__':
  main()
