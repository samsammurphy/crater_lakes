# PYTHON

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
  
  # correction coefficients at perihelion
  Edir, Edif, tau2, Lp = iLUT(i['solar_z'],i['H2O'],i['O3'],i['AOT'],i['alt'])
  
  # elliptical orbit correction
  Edir = Edir * simple_harmonic(i['doy'], 0.0327505,   18.99181408 ,  0.96804793)
  Edif = Edif * simple_harmonic(i['doy'], 0.03275025,  18.99238934 ,  0.96805088)
  Lp   = Lp   * simple_harmonic(i['doy'], 0.0327459 ,  18.99219987 ,  0.96804217)
  
  #surface reflectance
  ref = (math.pi*(radiance-Lp))/(tau2*(Edir+Edif))
  
  return ref