"""
Calculates surface reflectance using iLUT

(harmonic function is used to correct for elliptical orbit of Earth)

"""

import numpy as np
import math


def simple_harmonic(doy, a,b,c): 
  """
  harmonic function for elliptical orbit correction
  """
  return a*np.cos(doy/(b*math.pi)) + c


def surface_reflectance(radiance, iLUT, i):
  """
  surface reflectance from at-sensor radiance and other inputs
  """
  
  # at perihelion
  Edir, Edif, tau2, Lp = iLUT(i['solar_z'],i['H2O'],i['O3'],i['AOT'],i['alt'])
  
  # day of year correction coefficients
  a = 0.03275
  b = 18.992
  c = 0.968047
  
  # apply elliptical orbit correction
  Edir = Edir * simple_harmonic(i['doy'],a,b,c)
  Edif = Edif * simple_harmonic(i['doy'],a,b,c)
  Lp   = Lp   * simple_harmonic(i['doy'],a,b,c)
  
  #surface reflectance
  ref = (math.pi*(radiance-Lp))/(tau2*(Edir+Edif))
  
  return ref