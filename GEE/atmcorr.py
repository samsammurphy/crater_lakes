


def simple_harmonic(doy, a,b,c): 
  """
  harmonic function for elliptical orbit correction
  """
  return a*np.cos(doy/(b*math.pi)) + c


def surface_reflectance(L, iLUTx, v, model_AOT, alt):
  
  # correction coefficients at perihelion
  Edir, Edif, tau2, Lp = iLUTx(v['solar_z'],v['H2O'],v['O3'], model_AOT, alt)
  
  # elliptical orbit correction
  doy = doy_from_timestamp(v['timestamp'])
  Edir = Edir * simple_harmonic(doy, 0.0327505,   18.99181408 ,  0.96804793)
  Edif = Edif * simple_harmonic(doy, 0.03275025,  18.99238934 ,  0.96805088)
  Lp   = Lp   * simple_harmonic(doy, 0.0327459 ,  18.99219987 ,  0.96804217)
  
  #surface reflectance
  ref = (math.pi*(L-Lp))/(tau2*(Edir+Edif))
  
  return ref