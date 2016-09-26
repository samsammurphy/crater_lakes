import re
from target_altitudes import target_altitudes

def set_scene_info(target,satID,solar_z,H2O,O3,doy):
  
  #altitude (km)
  altitude = target_altitudes()[target]
  
  # sensor name from satID
  if re.search('4',satID) != None:
    sensor = 'LANDSAT_TM'
  elif re.search('5',satID) != None:
    sensor = 'LANDSAT_TM'
  elif re.search('7',satID) != None:
    sensor = 'LANDSAT_ETM'# the '+' is implied (i.e. ETM+)
  elif re.search('8',satID) != None:
    sensor = 'LANDSAT_OLI'
  else:
    print('sensor not recognized') 
    
  # band names
  band_names = ['blue','green','red','nir','swir1','swir2']
  
  # scene information
  scene_info = {
  'target':target,
  'band_names':band_names,
  'sensor':sensor,
  'solar_z':solar_z,
  'H2O':H2O,
  'O3':O3,
  'doy':doy,
  'alt':altitude
  }
  
  return scene_info