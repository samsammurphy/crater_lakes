"""
Calculates surface reflectance of crater lakes from GEE exported time series

Output is considered to be final result

"""



"""
TODO! Add the (dT) thermal atmospheric correction here!

ensure that you are using the correct gradient for each tir waveband
"""

import os
import glob
import json
import pickle

import numpy

from target_altitude import target_altitude
from surface_reflectance import surface_reflectance



def load_iLUTs(satellite,aerosol):
  """
  Load iLUTs for a given satellite and aerosol profile
  """
  
  base_path = '/home/sam/git/crater_lakes/atmcorr/iLUTs/'
  
  sensor_name = {
               'AST':'ASTER',
               'L4':'LANDSAT_TM',
               'L5':'LANDSAT_TM',
               'L7':'LANDSAT_ETM',
               'L8':'LANDSAT_OLI'
               }
               
  path = os.path.join(base_path,sensor_name[satellite]+'_'+aerosol,'viewz_0/')

  fnames = sorted(glob.glob(path+'*.ilut'))
  
  band_names = ['blue','green','red','nir','swir1','swir2']
  
  if satellite == 'AST':
    band_names = ['green','red','nir','swir1','swir2','swir3','swir4','swir5','swir6']
    
  iLUTs = {}
  
  for i, fname in enumerate(fnames):
    iLUTs[band_names[i]] = pickle.load(open(fname, "rb" ))
  
  return iLUTs


import numpy as np
from surface_reflectance import surface_reflectance



def estimate_lake_AOT(vnir,swir,params, iLUTs):
  """
  Estimates aerosol optical thickness over crater lake using the water pixel 
  ratio method (Kaufmann et al. 2008)
  
  swir / nir = 0.81
  
  where,  
  nir = near infrared radiance at 0.8 microns
  swir = short-wave infrared radiance 2.2 microns
  """
  
  # define 2.2 micron swir band
  if params['satellite'] == 'AST':
    swir_band = 'swir3'
  else:
    swir_band = 'swir2'
    
  # define model values for AOT
  model_values = [0.001]
  while np.max(model_values)*1.05 < 3:
    model_values.append(np.max(model_values)*1.05) 
  
  # calculate (potential) surface reflectance ratios for each model AIT value
  ratios = []
  for AOT in model_values:
    
    params['AOT'] = AOT # set model value to params dic 

    srNir = surface_reflectance(vnir['nir'], iLUTs['nir'],params)
    
    srSwir = surface_reflectance(swir[swir_band], iLUTs[swir_band],params)
    
    ratios.append(srSwir / srNir)
       
  # Find best result (i.e. where ratio closest to 0.81)
  delta = abs(np.array(ratios)-0.81)
  index = np.where(delta == np.min(delta))[0][0]
  match = model_values[index]
    
  return match

  
  
def atmospherically_correct_time_series(target, satellite, aerosol):
  """
  Apply atmospheric correction over a time series for a given target and satellite 
  """
   
  base_path = '/home/sam/git/crater_lakes/atmcorr/lake_data/'
    
  with open(base_path+'{0}/{1}_{0}.geojson'.format(target,satellite)) as f: 
    GEE_data = json.load(f)
  
  iLUTs = load_iLUTs(satellite,aerosol)
  
  altitude = target_altitude(target)
  
  results = []
  
  for feature in GEE_data['features']:
     
    properties = feature['properties']
    
    vnir = properties['vnir']['mean_radiance']
    swir = properties['swir']
        
    # validity testing
    valid = True
    if properties['vnir']['pixel_counts']['lake'] == 0: # lake pixels found?
      valid = False
    if properties['solar_z'] > 60: 
      valid = False
    if not swir['swir1']: # i.e. both ASTER and LANDSAT SWIR can be OFF
      valid = False
    # TODO catch no data (?)
    
    if valid:
      
      print(properties)
         
      params = {
                'solar_z':properties['solar_z'],
                'H2O':properties['H2O'],
                'O3':properties['O3'],
                'alt':altitude,
                'doy':properties['doy'],
                'satellite':satellite
                }
      

             
      params['AOT'] = estimate_lake_AOT(vnir,swir,params,iLUTs)
         
      sr = {} # surface reflectance
  
      # VNIR    
      for band in ['blue','green','red','nir']:
        try:
          radiance = vnir[band]
          sr[band] = surface_reflectance(radiance, iLUTs[band], params)
        except:
          pass
    
      # SWIR
      for band in ['swir1','swir2','swir3','swir4','swir5','swir6']:
        try:
          radiance = swir[band]
          sr[band] = surface_reflectance(radiance, iLUTs[band], params)
        except:
          pass
      
      # Timestamp
      unix_time = properties['date']['value'] / 1000 # i.e. GEE uses milliseconds
        
      result = {
                'fileID': feature['id'],
                'timestamp': unix_time, 
                'sr':sr
                }
        
      results.append(result)    

  # chronological sort 
  def chronological(dictionary): return dictionary['timestamp']
  results = sorted(results,key=chronological)
  
  return results
  
def pickle_result(result, target, satellite):
  
  outdir = "/home/sam/git/crater_lakes/atmcorr/results/"+target
  try:
    os.chdir(outdir)
  except:
    os.mkdir(outdir)
    os.chdir(outdir)
    
  pickle.dump(result,open("{}_{}.p".format(target,satellite),"wb"))


  
def main():
  
  target = 'Aoba'
  
  satellite = 'L7'
  
  aerosol = 'MA'# TODO CO needs interpolation for ASTER and other LANDSATs
     
  result = atmospherically_correct_time_series(target, satellite, aerosol)
  
  pickle_result(result, target, satellite)
  
  print('done')
      
if __name__ == '__main__':
  main()