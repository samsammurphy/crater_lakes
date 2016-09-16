
import csv
import datetime

def read_lake_time_series(filepath):
  
  #read data into this list  
  data = []
  
  with open(filepath, 'r') as csvfile:
  
    reader = csv.reader(csvfile, delimiter=',')
    header = next(reader, None) 
    for row in reader:
      
      # fileID (called 'system:index' in GEE (however, ':' is an illegal character for variables in python)    
      fileID = row[header.index('system:index')]
      
      # date
      string_date = (row[header.index('date')])
      date = datetime.datetime.strptime(string_date,'%Y-%m-%dT%H:%M:%S')
      
      # day of year (decimal)
      doy = float(row[header.index('doy')])
      
      # number of lake pixels detected
      lake_count = int(float(row[header.index('lake_pixel_count')]))
      
      # number of cloud pixels detected
      cloud_count = int(float(row[header.index('cloud_count')]))
      
      # mean radiance values
      lake_rad = {}    
      string_lake_rad = row[header.index('lake_mean_rad')]
      split = string_lake_rad[1:-1].split(',')
      for s in split:
        keyvalue = s.split('=')
        lake_rad[keyvalue[0]] = keyvalue[1]
      
      # solar zenith angle
      solar_z = float(row[header.index('solar_z')])
      
      # water vapour in atmosphere
      H2O = float(row[header.index('H2O')])
      
      # ozone in atmosphere
      O3 = float(row[header.index('O3')])
      
      data.append((fileID, date, doy, lake_count, cloud_count, lake_rad, solar_z, H2O, O3))
    
  #organize data into a dictionary (NB neater doing it this way then iterating list.append)
  output = {
  'fileIDs':    [d[0] for d in data],
  'date':       [d[1] for d in data],
  'doy':        [d[2] for d in data],
  'lake_count': [d[3] for d in data],
  'cloud_count':[d[4] for d in data],
  'lake_rad':   [d[5] for d in data],
  'solar_z':    [d[6] for d in data],
  'H2O':        [d[7] for d in data],
  'O3':         [d[8] for d in data] 
  }
    
  return output


filepath = '/home/sam/Desktop/Ldata_Aoba/L5_Aoba.csv'
print(read_lake_time_series(filepath))
    

    



