import ee

def round_date(date,xhour):
  """
  rounds a date of to the closest 'x' hours
  """
  y = date.get('year')
  m = date.get('month')
  d = date.get('day')
  H = date.get('hour')
  HH = H.divide(xhour).round().multiply(xhour)
  return date.fromYMD(y,m,d).advance(HH,'hour')


def get_water_vapour(geom,date):
  """
  Water vapour column above target at time of image aquisition.
  
  (Kalnay et al., 1996, The NCEP/NCAR 40-Year Reanalysis Project. Bull. 
  Amer. Meteor. Soc., 77, 437-471)
  """
  
  # Point geometry required
  centroid = geom.centroid()
  
  # H2O datetime is in 6 hour intervals
  H2O_date = round_date(date,6)
  
  #filtered water collection
  water_ic = ee.ImageCollection('NCEP_RE/surface_wv').filterDate(H2O_date)
  
  #water image
  water_img = ee.Image(water_ic.first())
  
  #water_vapour at target
  water = water_img.reduceRegion(reducer=ee.Reducer.mean(), geometry=centroid).get('pr_wtr')
                                      
  #convert to Py6S units (Google = kg/m^2, Py6S = g/cm^2)
  water_Py6S_units = ee.Number(water).divide(10)                                   
  
  return water_Py6S_units

def get_ozone(geom,date):
  """
  Returns ozone measurement from merged TOMS/OMI dataset
  
  OR
  
  Fill value during TOMS hiatus (and whereever else a fill value might occur)
  
  """
  
  # Point geometry required
  centroid = geom.centroid()
     
  def ozone_measurement(centroid,O3_date):
    
    # filtered ozone collection
    ozone_ic = ee.ImageCollection('TOMS/MERGED').filterDate(O3_date)
    
    # ozone image
    ozone_img = ee.Image(ozone_ic.first())
    
    # ozone value IF TOMS/OMI image exists ELSE use fill value
    ozone = ee.Algorithms.If(ozone_img,\
    ozone_img.reduceRegion(reducer=ee.Reducer.mean(), geometry=centroid).get('ozone'),\
    ozone_fill(centroid,O3_date))
    
    return ozone
    
  def ozone_fill(centroid,O3_date):
    
    # ozone fills (i.e. one band per doy)
    ozone_fills = ee.ImageCollection('users/samsammurphy/public/ozone_fill').toList(366)
    
    # day of year index
    jan01 = ee.Date.fromYMD(O3_date.get('year'),1,1)
    doy_index = date.difference(jan01,'day').toInt()# (NB. index is one less than doy, so no need to +1)
    
    # day of year image
    fill_image = ee.Image(ozone_fills.get(doy_index))
    
    # return scalar fill value
    return fill_image.reduceRegion(reducer=ee.Reducer.mean(), geometry=centroid).get('ozone')
   
  def ozone_main():
    
    # O3 datetime in 24 hour intervals
    O3_date = round_date(date,24)
    
    # TOMS temporal gap
    TOMS_gap = ee.DateRange('1994-11-01','1996-08-01')  
    
    # avoid TOMS gap entirely
    ozone = ee.Algorithms.If(TOMS_gap.contains(O3_date),ozone_fill(centroid,O3_date),ozone_measurement(centroid,O3_date))
    
    # fix other data gaps (e.g. spatial, missing images, etc..)
    ozone = ee.Algorithms.If(ozone,ozone,ozone_fill(centroid,O3_date))
    
    #convert to Py6S units 
    ozone_Py6S_units = ee.Number(ozone).divide(1000)# (i.e. Dobson units are milli-atm-cm )                             
    
    return ozone_Py6S_units
    
  return ozone_main()

