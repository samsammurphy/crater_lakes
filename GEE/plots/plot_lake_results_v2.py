import os 
import pickle
import numpy as np
from matplotlib import pylab as plt
import datetime


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
  
  datetime = [d['date'] for d in data]

  refs = [d['refs'] for d in data ]
  
  b = np.array([ref['blue'] for ref in refs])
  g = np.array([ref['green'] for ref in refs])
  r = np.array([ref['red'] for ref in refs])
  n = np.array([ref['nir'] for ref in refs])
  s1 = np.array([ref['swir1'] for ref in refs])
  s2 = np.array([ref['swir2'] for ref in refs])
  
  return {
  'datetime':datetime,
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
  
  datetime = [v['date'] for v in valid]
  
  thermal = [v['thermal'] for v in valid]
  
  bkgd_BT = np.array([t['bkgd_BT'] for t in thermal])
  bkgd_TIR = np.array([t['bkgd_TIR'] for t in thermal])
  lake_BT = np.array([t['lake_BT'] for t in thermal])
  lake_TIR = np.array([t['lake_TIR'] for t in thermal])

  dT = lake_BT - bkgd_BT #temperature above background
  
  fileID = [v['fileID'] for v in valid]
  
  return {
  'datetime':datetime,
  'bkgd_BT': bkgd_BT,
  'bkgd_TIR':bkgd_TIR,
  'lake_BT': lake_BT,
  'lake_TIR':lake_TIR,
  'dT':dT,
  'fileID':fileID
  }



# data
data = get_data('Aoba')
vswir = extract_vswir(data)
tir = extract_thermal(data)

# Visible RGB
plt.plot(vswir['datetime'],vswir['red'],'red')
plt.plot(vswir['datetime'],vswir['green'],'green')
plt.plot(vswir['datetime'],vswir['blue'],'blue')
plt.title('Visible RGB')
plt.show()

# figure object
fig = plt.figure()

# two axes objects
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()

# left-hand axes (Value and Saturation)
ax1.plot(vswir['datetime'],vswir['value'],'black', label = 'value')
ax1.plot(vswir['datetime'],vswir['saturation'],'gray', label = 'saturation')
ax1.set_ylabel('unitless')
ax1.set_ylim(0,0.6)

# right-hand axes (Temperature above background)
ax2.plot(tir['datetime'],tir['dT'],'red', label = 'temperature')
ax2.set_ylabel(r"$\Delta$T ($^\circ$C)")
ax2.set_ylim(-5, 15)

# x-axis
ax1.set_xlabel("Time")
ax1.set_xlim(datetime.datetime(1990,1,1),datetime.datetime(2016,1,1))

# separate legends
#ax1.legend(loc=2)
#ax2.legend(loc=1)

# joint Legend
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc=0)

# Done
ax1.grid()
plt.show()




