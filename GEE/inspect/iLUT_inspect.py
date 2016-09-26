

import os
import glob
import pickle


def load_iLUTs_in_path(path):
  """
  loads iLUTs in a given path..
  paths are unique for each unique set of (sensor, aerosol, view_z)
  """
  
  fnames = glob.glob(path+'*.ilut')
  fnames.sort()
    
  iLUTs = {
  'blue' : pickle.load(open(fnames[0], "rb" )),
  'green': pickle.load(open(fnames[1], "rb" )),
  'red'  : pickle.load(open(fnames[2], "rb" )),
  'nir'  : pickle.load(open(fnames[3], "rb" )),
  'swir1': pickle.load(open(fnames[4], "rb" )),
  'swir2': pickle.load(open(fnames[5], "rb" ))
  }

  return iLUTs

def load_iLUTs(aerosol):
  """
  Loads iLUTs for (multiple) sensors and a single aerosol profile
  """
  
  base_path = '/home/sam/git/crater_lakes/GEE/atmcorr/iLUTs/'
  
  sensors = ['LANDSAT_TM','LANDSAT_ETM','LANDSAT_OLI']
  
  iLUTs = dict()
  for sensor in sensors:
    path = os.path.join(base_path,sensor+'_'+aerosol,'viewz_0/')
    iLUTs[sensor] = load_iLUTs_in_path(path)
  
  return iLUTs


def print_output(sensor,waveband):
  output = iLUTs[sensor][waveband](solar_z,H2O,O3,AOT,alt)
  print('{0[0]:06.4f}  {0[1]:05.4f}  {0[2]:03.4f}  {0[3]:03.4f}'.format(output))


iLUTs = load_iLUTs('MA')

#testing
solar_z = 20
H2O = 0
O3 = 0.8
AOT = 0
alt = 0
waveband = 'blue'

print('waveband = ',waveband)
print('Edir     Edif    tau2  Lp')
print_output('LANDSAT_TM',waveband)
print_output('LANDSAT_ETM',waveband)
print_output('LANDSAT_OLI',waveband)