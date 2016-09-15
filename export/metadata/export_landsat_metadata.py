# -*- coding: utf-8 -*-
"""
Landsat metadata to .CSV in Google Drive

INCLUDING atmospheric conditions (H2O and O3)

(altitudes are extracted separately because they are i) constant ii) not all in SRTM)

- file ID
- datetime
- H20
- O3 (merged OMI and TOMS)
- solar zenith
- view zenith

"""

import ee

#Initialize Google Earth Engine API
ee.Initialize()

#Landsat metadata
#------------------------------------------------------------------------------


#function to extract metadata from Landsat
#TODO export solar zenith directly, use null geometries (to save space)
def getMetadata(img):
  time = img.get('SCENE_CENTER_TIME')
  solar_e = img.get('SUN_ELEVATION')
  #solar_z = 90-solar_e
  satellite = img.get('SPACECRAFT_ID')
  view_z = img.get('ROLL_ANGLE')# //Landsats 1-7 are always NADIR (empty csv) LANDSAT 8 will have a roll angle (-90 to +90)
  return ee.Feature(None,{satellite:satellite,time:time,solar_e:solar_e,view_z:view_z})
  #return ee.Feature(geom,{satellite:satellite,time:time,solar_z:solar_z,view_z:view_z})


# Atmospheric metadata
#------------------------------------------------------------------------------
#TODO add H2O and O3


def main():
  
  #all geometries
  geoms = ee.FeatureCollection('ft:12PQq9qXwrGs_GOwaL8XtNvYEPnbhW7ercpiIFv0h')
  
  #target properties
  target_name = 'Anatahan'
  geom = geoms.filter(ee.Filter.equals('name', target_name)).geometry()
  
  # metadata feature collection from landsat image collections
  # TODO add other collecitons
  L7 = ee.ImageCollection('LANDSAT/LE7_L1T').filterBounds(geom).map(getMetadata)
  print(L7)

#  # export the feature collection
#  Export.table.toDrive(L7, target_name, 'Landsat_metadata')

if __name__ == '__main__':
  main()

