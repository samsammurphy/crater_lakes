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
    



