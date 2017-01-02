"""
Reads target altitude from .csv

"""


import numpy as np

def target_altitude(target):
  """
  Altitude of target locations (in metres) 
  
  source: Shuttle Radar Topography Mission (SRTM), except for Askja, Grimsovtn 
  and Spurr which are from Google Earth (not sure what source they used).
  
  """
  
  #path to altitudes csv
  fpath = '/home/sam/git/crater_lakes/GEE/atmcorr/altitudes_full.csv'
  
  # read csv
  targets,str_alts = np.genfromtxt(fpath, dtype='str', unpack=True, \
    skip_header=1, delimiter=',')
    
  #convert altitude to float and to km
  altitudes = [float(alt)/1000 for alt in str_alts]
  
  # dictionary
  dic = dict(zip(list(targets),list(altitudes)))
   
  return dic[target]