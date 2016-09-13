# -*- coding: utf-8 -*-
"""

Gathers the inputs needed for atmospheric correction into a single csv

takes in 
- altitude
- file metadata
- H2O
- O3
- mean at-sensor radiance (cloud-free) of nir and swir2 (i.e. for AOT retrieval)

matches using fileID or UNIX time

"""

import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as dt
import csv

# file locations
def get_filepaths(target):
  alt = '/media/sam/DataDisk/GoogleDrive/Volcanoes/altitudes/altitudes_full.csv'
  metadata = '/media/sam/DataDisk/GoogleDrive/Data/Landsat/_Landsat_metadata/'+target+'.csv'
  H2O = '/home/sam/Dropbox/HIGP/Crater_Lakes/preprocessing/atmospheric_correction/parameters/water_vapour/GEE_water_vapour/'+target+'.csv'
  O3 = '/home/sam/Dropbox/HIGP/Crater_Lakes/preprocessing/atmospheric_correction/parameters/ozone/GEE_ozone/'+target+'.csv'
  AOT_rads = '/media/sam/DataDisk/GoogleDrive/Data/Landsat/AOT_retrieval/water_stats_for_AOT_'+target+'_full.csv'
  return {'alt':alt,'metadata':metadata,'H2O':H2O,'O3':O3,'AOT_rads':AOT_rads}

# generic csv reader
def read_csv(filepath):
    return np.genfromtxt(filepath,dtype='str',unpack=True,skip_header=1,delimiter=',')
    
# timestamps of satellite scenes
def scene_timestamp(fileID, time):
  
  #year and day-of-year from fileID
  y = int(fileID[9:13]) 
  doy = int(fileID[13:16])
  
  #date
  date = datetime.datetime(y, 1, 1) + datetime.timedelta(doy - 1)
  
  #time
  t = time.split(':')
  H = int(t[0])               # hours
  M = int(t[1])               # minutes
  S = round(float(t[2][:-1])) # seconds
  time = datetime.timedelta(hours=H,minutes=M,seconds=S)
    
  #datetime
  this_datetime = date+time
    
  return this_datetime.timestamp()

# read satellite metadata file
def read_metadata(filepath):
  METADATA = read_csv(filepath)
  
  fileIDs = list()
  metadata = list()
  for i in range(0,len(METADATA[0])):
    
    fileID = METADATA[0][i]
    time = METADATA[3][i]
    timestamp = scene_timestamp(fileID,time)
    solar_z = 90-float(METADATA[2][i])
    view_z = METADATA[4][i]
    if view_z == '':
      view_z = 0
    else:
      view_z = float(view_z)
    
    fileIDs.append(fileID)
    metadata.append({'timestamp':timestamp,'solar_z':solar_z,'view_z':view_z})
  
  return dict(zip(list(fileIDs),list(metadata)))
  
def read_alts(filepath):
  targets,altitudes = read_csv(filepath)
  
  return dict(zip(list(targets),list(altitudes)))
  
def read_H2O(filepath):
  H2O_raw = read_csv(filepath)
  data_IDs = H2O_raw[0]
  data_values = H2O_raw[1]

  timestamps = list()
  for data_ID in data_IDs:
    ymdH = data_ID[12:22] # year+month+day+hour
    this_datetime = datetime.datetime.strptime(ymdH,'%Y%m%d%H')    
    timestamps.append(this_datetime.timestamp())  
    
  values = list()
  for data_string in data_values:
    s = data_string.split('=')
    values.append(float(s[1][:-2]))
    
  return {'timestamps':timestamps,'H2O':values}

def read_O3(filepath):
  O3_raw = read_csv(filepath)
  data_IDs = O3_raw[0]
  data_values = O3_raw[1]

  # datetime
  timestamps = list()
  doys = list()      # required for null handling
  for data_ID in data_IDs:
    s = data_ID.split('_')
    this_datetime = datetime.datetime.strptime(s[-1],'%Y%m%d')
    timestamps.append(this_datetime.timestamp())
    y = int(this_datetime.strftime('%Y'))
    doy = this_datetime - datetime.datetime(y, 1, 1) + datetime.timedelta(1)
    doys.append(doy.days)
  
  # values (handle null)
  values = list()
  for data_string in data_values:
    s = data_string.split('=')
    value = s[1][:-2]
    if value[0] == 'n':
      value = 0
    values.append(float(value))
  
  # replace null values with mean for that doy
  doys = np.array(doys)
  values = np.array(values)
  bad = list(np.where(values == 0)[0])
  for b in bad:
    this_doy = doys[b]
    these_doy_values = values[np.where(this_doy == doys)]
    valid_values = these_doy_values[np.where(these_doy_values > 0)[0]]
    values[b] = np.mean(valid_values)
  
  return  {'timestamps':timestamps,'O3':values,'doys':doys}
  
# statistics of lake water used for AOT retrieval
def read_AOT_stats(filepath):
  AOT_data = read_csv(filepath)
  
  fileIDs = list()
  AOT_stats = list()

  for i in range(0,len(AOT_data[0])):
    
    fileID = str(AOT_data[0][i]).split('_')[-1]
    stats = [
    AOT_data[1][i].split('=')[-1],      # count_nir
    AOT_data[2][i].split('=')[-1],      # count_swir2
    AOT_data[3][i].split('=')[-1][:-2], # count_ndwi
    AOT_data[4][i].split('=')[-1],      # mean_nir
    AOT_data[5][i].split('=')[-1],      # mean_swir2
    AOT_data[6][i].split('=')[-1][:-2]  # mean_ndwi   
    ]

    fileIDs.append(fileID)
    AOT_stats.append(stats)

  return dict(zip(fileIDs,AOT_stats))

def valuefromTimestamp(data,value_name,timestamp):
  
  #H2O / O3 values and timestamps
  values = data[value_name]
  timestamps = data['timestamps']
  
  # minimum absolute difference match
  diff = abs(np.array(timestamps)-timestamp)
  match = np.where(diff == min(diff))[0]
  if len(match > 1):
    match = match[0]
  
  return values[match]

# target
target = "Aoba" 

# filepaths for this target
filepaths = get_filepaths(target)

# satellite metadata
metadata = read_metadata(filepaths['metadata'])

# altitude
target_alts = read_alts(filepaths['alt'])

# H2O
H2Os = read_H2O(filepaths['H2O'])

# O3
O3s = read_O3(filepaths['O3'])

# AOT_rads
AOT_stats = read_AOT_stats(filepaths['AOT_rads'])


# save to new csv file
filename = open('/home/sam/Desktop/Aoba_atmcorr_inputs.csv',"w")
writer = csv.writer(filename)
writer.writerow(["Altiude = "+target_alts[target]+'  | columns =  fileID,timestamp,solar_z,view_z,H2O,O3,AOT_stat'])
fileIDs = list(metadata.keys())
for fileID in fileIDs:
  
  timestamp = metadata[fileID]['timestamp']
  solar_z = metadata[fileID]['solar_z']
  view_z = metadata[fileID]['view_z']
  H2O = valuefromTimestamp(H2Os,'H2O',timestamp)
  O3 = valuefromTimestamp(O3s,'O3',timestamp)
  try:
    AOT_stat = AOT_stats[fileID]
    writer.writerow([fileID,timestamp,solar_z,view_z,H2O,O3,AOT_stat])
  except:
    print('missing fileID: ',fileID)
