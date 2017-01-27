"""
ASTER_spectral_library_reader.py, author: Sam Murphy (2016-10-17)

Reads spectra from the ASTER Spectral Library

"""

import glob
import os
import re
from matplotlib import pylab as plt

# finds all spectra in a given group
def find_spectra(spectral_group):
  rootdir = '/home/sam/Dropbox/HIGP/Crater_Lakes/TIR/spectra/'
  f = glob.glob(rootdir+'/'+spectral_group+'/*')
  return f
  
  # read spectral file
def read_spectrum(path):
  f = open(path,'r')
  spectra = re.findall(r'\s+([\d.]+)\s+([\d.]+)',f.read())
  wavelengths = [w for w,r in spectra]
  reflectance = [r for w,r in spectra]
  return(wavelengths,reflectance)

def plot_spectra(spectral_group): 
  # figure with single subplot (i.e. to fit legend outside of graph)  
  fig = plt.figure()
  ax = plt.subplot(111)
  
  # properties of axis
  ax.set_title(spectral_group)
  ax.set_xlabel('wavelength (microns)')
  ax.set_ylabel('reflectance')
  ax.set_xlim(8,14)
  ax.set_ylim(0,20)
  
  # plot each spectra
  paths = find_spectra(spectral_group)
  for path in paths:
    spectrum = read_spectrum(path)
    ax.plot(spectrum[0],spectrum[1],label=os.path.basename(path))
  
  #legend outside of plot
  box = ax.get_position()# i.e. first shrink this axis object
  ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
  ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
  
  # plot waveband
  ax.plot([11,11],[0,20],'--r')
  
  fig.show()
  

# spectral plot type
plot_spectra('vegetation')