"""
Reads time series information from (GEE exported) .csv file

Parameters include:
- fileID
- date and doy
- lake,  cloud and valid pixel counts
- lake radiances
- solar_z, H20, O3
- LEDAPS (SR + cfmask)
- TIR radiance and brightness temperatures


"""


import re
import csv
import datetime


def list_to_dictionary(string_list,dictionary):
  
  split = string_list.split(',')
  for s in split:
    keyvalue = s.split('=')
    key = keyvalue[0].strip()
    value = keyvalue[1].strip() 
    if 'null' in value:
      dictionary[key] = None
    else:
      dictionary[key] = float(value)
  
  return dictionary
  

def parse_string_dict(string_dict):

  #remove {} from string dictionary
  string_list = string_dict[1:-1]
  
  #return python dictionary
  return list_to_dictionary(string_list,{})

  
def parse_LEDAPS(row,header):
  
  # read csv string
  string = row[header.index('LEDAPS')][1:-1]

  #LEDAPS dictionary
  LEDAPS = {}   
    
  #search for lake_SR dict in string
  match = re.search('lake_SR=',string)
  
  #extract pixel counts
  counts = string[:match.span()[0]-2]
  LEDAPS = list_to_dictionary(counts,LEDAPS)
  
  #check LEDAPS image exists
  if LEDAPS['water_count'] == None:
    return None
  
  #check water pixels were found
  if LEDAPS['water_count']:
    lake_SR_dict = string[match.span()[1]:]
    LEDAPS['lake_SR'] = parse_string_dict(lake_SR_dict)
  else:
    LEDAPS['lake_SR'] = None
   
  return LEDAPS

def read_lake_time_series(filepath):
  
  #read data into this list  
  data = []
  
  with open(filepath, 'r') as csvfile:
  
    reader = csv.reader(csvfile, delimiter=',')
    header = next(reader, None) 
    
    if len(header) == 0:
      return None
    
    for row in reader:
           
      # fileID (called 'system:index' in GEE (however, ':' is an illegal character for variables in python)    
      fileID = row[header.index('system:index')]
      
      # date
      string_date = (row[header.index('date')])
      date = datetime.datetime.strptime(string_date,'%Y-%m-%dT%H:%M:%S')
      
      # day of year (decimal)
      doy = float(row[header.index('doy')])
      
      # number of lake pixels detected
      lake_count = int(float(row[header.index('lake_count')]))
      
      # number of cloud pixels detected
      cloud_count = int(float(row[header.index('cloud_count')]))
      
      # valid pixel count
      valid_count = parse_string_dict(row[header.index('valid_count')])
      
      # mean radiance values
      lake_rad = parse_string_dict(row[header.index('lake_mean_rad')])
        
      # solar zenith angle
      solar_z = float(row[header.index('solar_z')])
      
      # water vapour in atmosphere
      H2O = float(row[header.index('H2O')])
      
      # ozone in atmosphere
      O3 = float(row[header.index('O3')])
      
      # LEDAPS
      LEDAPS = parse_LEDAPS(row,header)
      
      # Thermal infrared
      thermal = parse_string_dict(row[header.index('thermal')])
      
      # append results as a dictionary
      data.append({
      'fileID':fileID,
      'date':date,
      'doy':doy,
      'lake_count':lake_count,
      'cloud_count':cloud_count,
      'valid_count':valid_count,
      'lake_rad':lake_rad,
      'solar_z':solar_z,
      'H2O':H2O,
      'O3':O3,
      'LEDAPS':LEDAPS,
      'thermal':thermal
      })
   
  return data