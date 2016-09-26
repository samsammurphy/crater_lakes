import os 
import pickle
import numpy as np
from matplotlib import pylab as pl


def get_data(target):
  
  data_rootdir = '/home/sam/git/crater_lakes/GEE/atmcorr/time_series/'
  data_path = os.path.join(data_rootdir,target)
  
  all_data = []
  
  for satID in ['L4','L5','L7','L8']:
    data_file = '{}_{}.p'.format(target,satID)
    data = pickle.load(open(os.path.join(data_path,data_file),"rb"))
    if data:
      all_data = all_data + data
      
   # chronologically sort
  def date_sort_key(dic): return dic['date'].timestamp()
  all_data = sorted(all_data,key=date_sort_key)
  
  return all_data
  
  
def extract_thermal(data):
  
  # lake AND bkgd must exist
  valid = [d for d in data if d['thermal']['lake_BT'] and d['thermal']['bkgd_BT']]
  
  thermal = [v['thermal'] for v in valid]
  
  bkgd_BT = np.array([t['bkgd_BT'] for t in thermal])
  bkgd_TIR = np.array([t['bkgd_TIR'] for t in thermal])
  lake_BT = np.array([t['lake_BT'] for t in thermal])
  lake_TIR = np.array([t['lake_TIR'] for t in thermal])

  dT = lake_BT - bkgd_BT #temperature above background
  
  datetime = [v['date'] for v in valid]
  
  fileID = [v['fileID'] for v in valid]#(for playground inspection)
  
  return {
  'fileID':fileID,
  'datetime':datetime,
  'bkgd_BT': bkgd_BT,
  'bkgd_TIR':bkgd_TIR,
  'lake_BT': lake_BT,
  'lake_TIR':lake_TIR,
  'dT':dT
  }
    
    
    
data = get_data('Aoba')  
thermal = extract_thermal(data)
pl.plot(thermal['datetime'],thermal['lake_BT'],'blue',label='lake')
pl.plot(thermal['datetime'],thermal['bkgd_BT'],'green',label='bkgd')
pl.ylabel('Temperature (oC)')
pl.legend(loc='best')
pl.show()

pl.plot(thermal['datetime'],thermal['dT'],'red')
pl.title('Temperature Above Background')
pl.ylabel('dT')
