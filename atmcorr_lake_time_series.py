"""
Calculates surface reflectance of crater lakes from GEE exported time series

Output is considered to be final result

"""



"""
TODO! Add the (dT) thermal atmospheric correction here!

ensure that you are using the correct gradient for each tir waveband
"""

import os
import pickle

from target_altitude import target_altitude
from sensor_from_satID import sensor_from_satID
from read_GEE_export import read_lake_time_series
from iLUTs import load_iLUTs
from get_AOT import get_AOT
from surface_reflectance import surface_reflectance


def all_vswir_exists(data, vswirNames):
  for vswirName in vswirNames:
    if not data['lake_rad'][vswirName]:
      return 0
  return 1

def atmcorr_satellite_time_series(target, satID, all_iLUTs):
  """
  Atmospherically correct a time series of data for a given satellite
  """
  
  #satellite specifics
  sensor_iLUTs = all_iLUTs[sensor_from_satID(satID)]
  vswirNames = ['blue','green','red','nir','swir1','swir2']  
  
  # lake data for this target and satellite
  filepath = '/home/sam/git/crater_lakes/GEE/atmcorr/lake_data/{0}/{1}_{0}.csv'.format(target,satID)
  lake_data = read_lake_time_series(filepath)
  
  output = []
  i=0
  if lake_data:
  
    for data in lake_data:
      
      print(i,data['fileID'])
      i += 1
                                                   # MUST..
      if data['lake_count'] == 0:                  # 1) detect water pixels
        print('No lake water pixels found')        #
                                                   #
      elif data['solar_z'] > 60:                   # 2) have solar zenith < 60
        print('Solar zenith is > 60')              #
                                                   #
      elif all_vswir_exists(data, vswirNames) == 0:# 3) have all vswir channels
        print('Not all VSWIR channels available')  #
                                                   #
      else:                                        # ..to be valid..
      
        # add altitude to data
        data['alt'] = target_altitude(target)
          
        # AOT estimate
        data['AOT'] = get_AOT(data, sensor_iLUTs)
        
        # surface reflectance
        refs = {}
        for vswirName in vswirNames:
          radiance = data['lake_rad'][vswirName]
          iLUT = sensor_iLUTs[vswirName]
          refs[vswirName] = surface_reflectance(radiance, iLUT, data)
        
        data['refs'] = refs
        output.append(data)


  # sort chronologically 
  def datesort(dictionary): return dictionary['date'].timestamp()
  output = sorted(output,key=datesort)
  
  # save file
  indir = "/home/sam/git/crater_lakes/atmcorr/time_series/"+target
  try:
    os.chdir(indir)
  except:
    os.mkdir(indir)
    os.chdir(indir)
  pickle.dump(output,open("{}_{}.p".format(target,satID),"wb"))


def main():
  
  target = 'Aoba'
  
  aerosol = 'MA'
  
  # iLUTs for this target (i.e. aerosol type)
  all_iLUTs = load_iLUTs(aerosol)
  
  # atmospherically correct data from each satellite data stream
  satIDs = ['L4','L5','L7','L8']
  for satID in satIDs:
    atmcorr_satellite_time_series(target, satID, all_iLUTs)
      
main()