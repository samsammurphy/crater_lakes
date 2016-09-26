import re

def sensor_from_satID(satID):
    
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
    
  return sensor