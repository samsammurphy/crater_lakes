import os 
import pickle
import numpy as np
import datetime
from matplotlib import pylab as plt



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


def extract_vswir(data):
  
  date = [d['date'] for d in data]

  refs = [d['refs'] for d in data ]
  
  b = np.array([ref['blue'] for ref in refs])
  g = np.array([ref['green'] for ref in refs])
  r = np.array([ref['red'] for ref in refs])
  n = np.array([ref['nir'] for ref in refs])
  s1 = np.array([ref['swir1'] for ref in refs])
  s2 = np.array([ref['swir2'] for ref in refs])
  
  return {
  'date':date,
  'blue':b,
  'green':g,
  'red':r,
  'nir':n,
  'swir1':s1,
  'swir2':s2,
  'value':[max(ri,gi) for ri, gi in zip(r,g)],
  'saturation':(g-r),# not absolute so that you can see if g OR r is higher
  'greyness': 1 - abs(r-g)
  }

def extract_thermal(data):
  
  # valid scenes must contain lake AND bkgd TIR data
  valid = [d for d in data if d['thermal']['lake_BT'] and d['thermal']['bkgd_BT']]
  
  date = [v['date'] for v in valid]
  
  thermal = [v['thermal'] for v in valid]
  
  bkgd_BT = np.array([t['bkgd_BT'] for t in thermal])
  bkgd_TIR = np.array([t['bkgd_TIR'] for t in thermal])
  lake_BT = np.array([t['lake_BT'] for t in thermal])
  lake_TIR = np.array([t['lake_TIR'] for t in thermal])

  dT = lake_BT - bkgd_BT #temperature above background
  
  fileID = [v['fileID'] for v in valid]
  
  return {
  'date':date,
  'bkgd_BT': bkgd_BT,
  'bkgd_TIR':bkgd_TIR,
  'lake_BT': lake_BT,
  'lake_TIR':lake_TIR,
  'dT':dT,
  'fileID':fileID
  }

def pixel_counts(data):
  
  # count of pixels inside the geom
  valid_count = np.array([d['valid_count']['green'] for d in data ],dtype='float')
  
  # max valid count
  max_valid_count = np.max(valid_count)
  
  # valid scenes must have 95% of max number of pixels in geom
  valid = [d for d in data if d['valid_count']['green'] > 0.95*max_valid_count \
                           and d['cloud_count'] < 1000]
  
  # get data
  date = [v['date'] for v in valid]
  lake_count = np.array([v['lake_count'] for v in valid ],dtype='float')
  cloud_count = np.array([v['cloud_count'] for v in valid ],dtype='float')
  
  # convert to km2
  pixel_size = 900.
  lake_count *= pixel_size / 1e6
  cloud_count *= pixel_size / 1e6
  valid_count *= pixel_size / 1e6
  
  return {
  'date':date,
  'lake_count': lake_count,
  'cloud_count':cloud_count,
  'valid_count': valid_count,
  'max_valid_count':max_valid_count
  }


# data
data = get_data('Aoba')
vswir = extract_vswir(data)
tir = extract_thermal(data)
count = pixel_counts(data)

def plt_finish():
  plt.legend()
  plt.grid()
  plt.xlim(datetime.datetime(1990,1,1),datetime.datetime(2016,1,1))
  plt.show()

# visible
plt.plot(vswir['date'],vswir['red'],'red',label='red')
plt.plot(vswir['date'],vswir['green'],'green',label='green')
plt.plot(vswir['date'],vswir['blue'],'blue',label='blue')
plt.ylabel('surface reflectance')
plt_finish()

# value and saturation
plt.plot(vswir['date'],vswir['value'],'black', label = 'value')
plt.plot(vswir['date'],vswir['saturation'],'gray', label = 'saturation')
plt.ylabel('surface reflectance')
plt_finish()

# temperature
plt.plot(tir['date'],tir['dT'],'red')
plt.ylabel(r"$\Delta$T ($^\circ$C)")
plt_finish()

## size
plt.plot(count['date'],count['lake_count'],'blue',label='lake')
plt.plot(count['date'],count['cloud_count'],'grey',label='cloud')
plt.ylabel(r"area (km$^2$)")
plt_finish()
