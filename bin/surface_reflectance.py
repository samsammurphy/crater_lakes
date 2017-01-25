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


def surface_reflectance(radiance, iLUT, p):
  """
  surface reflectance from at-sensor radiance and other inputs
  """
  
  # at perihelion
  Edir, Edif, tau2, Lp = iLUT(p['solar_z'],p['H2O'],p['O3'],p['AOT'],p['alt'])
  
  # day of year correction coefficients
  a = 0.03275
  b = 18.992
  c = 0.968047
  
  # apply elliptical orbit correction
  Edir = Edir * simple_harmonic(p['doy'],a,b,c)
  Edif = Edif * simple_harmonic(p['doy'],a,b,c)
  Lp   = Lp   * simple_harmonic(p['doy'],a,b,c)
  
  #surface reflectance
  ref = (math.pi*(radiance-Lp))/(tau2*(Edir+Edif))
  
  return ref