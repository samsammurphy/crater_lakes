import ee

def get_water_vapour(geom,eeDate):
  """
  Water vapour column above target at time of image aquisition.
  
  (Kalnay et al., 1996, The NCEP/NCAR 40-Year Reanalysis Project. Bull. 
  Amer. Meteor. Soc., 77, 437-471)
  """
  
  # H2O datetime is hour closest to 0000, 0600, 1200, or 1800 UTC
  y = eeDate.get('year')
  m = eeDate.get('month')
  d = eeDate.get('day')
  H = eeDate.get('hour')
  HH = H.divide(6).round().multiply(6)
  H2O_datetime = ee.Date.fromYMD(y,m,d).advance(HH,'hour')
  
  #filtered water collection
  water_ic = ee.ImageCollection('NCEP_RE/surface_wv') \
    .filterDate(H2O_datetime)
  
  #water image
  water_img = ee.Image(water_ic.first())

  #water_vapour at target
  water = water_img.reduceRegion(reducer=ee.Reducer.mean(), geometry=geom).get('pr_wtr')
                                      
  #convert to Py6S units (Google = kg/m^2, Py6S = g/cm^2)
  water_Py6S_units = ee.Number(water).divide(10)                                   
  
  return water_Py6S_units

  
