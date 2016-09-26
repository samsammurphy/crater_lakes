
import pickle
import numpy as np
from matplotlib import pylab as pl

def Py6S_SR(channel):
  datetime = [d['date'] for d in data]
  SR = np.array([d['refs'][channel] for d in data ])
  return {'datetime':datetime,'SR':SR}

def LEDAPS_SR(channel):
  valid = [d for d in data if d['LEDAPS'] and d['LEDAPS']['water_count'] > 0] # filter LEDAPS = 0 or lake count = 0
  #datetime
  datetime = [v['date'] for v in valid]
  #surface reflectance
  SR = np.array([v['LEDAPS']['lake_SR'][channel] for v in valid])
  #file ID (for playground inspection)
  fileID = [v['fileID'] for v in valid]
  return {'datetime':datetime,'SR':SR,'fileID':fileID}
 
def plot_comparison(channel,color):
  Py6S = Py6S_SR(channel)
  LEDAPS = LEDAPS_SR(channel)
  
  pl.plot(Py6S['datetime'],Py6S['SR'],color)
  pl.plot(LEDAPS['datetime'],LEDAPS['SR'],'.r')
  pl.title(channel)
  pl.ylabel('surface reflectance')
  pl.xlabel('date')
  pl.show()



data = pickle.load(open("/home/sam/git/crater_lakes/GEE/atmcorr/time_series/Aoba/Aoba_L7.p","rb"))

plot_comparison('blue','-b')
#plot_comparison('green','-g')
#plot_comparison('red','-r')
#plot_comparison('nir','-m')
#plot_comparison('swir1','-c')
#plot_comparison('swir2','-y')


#z = list(zip(LEDAPS['fileID'],LEDAPS['SR']))
#print(z)