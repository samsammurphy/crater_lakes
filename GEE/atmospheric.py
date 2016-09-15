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
  
  # H2O datetime is in 6 hour intervals
  H2O_date = round_date(date,6)
  
  #filtered water collection
  water_ic = ee.ImageCollection('NCEP_RE/surface_wv').filterDate(H2O_date)
  
  #water image
  water_img = ee.Image(water_ic.first())

  #water_vapour at target
  water = water_img.reduceRegion(reducer=ee.Reducer.mean(), geometry=geom).get('pr_wtr')
                                      
  #convert to Py6S units (Google = kg/m^2, Py6S = g/cm^2)
  water_Py6S_units = ee.Number(water).divide(10)                                   
  
  return water_Py6S_units

def get_ozone(geom,date,fill):
     
  def ozone_measurement(geom,O3_date):
    
    #filtered ozone collection
    ozone_ic = ee.ImageCollection('TOMS/MERGED').filterDate(O3_date)
    
    #ozone image
    ozone_img = ee.Image(ozone_ic.first())
    
    #ozone column over target
    return ozone_img.reduceRegion(reducer=ee.Reducer.mean(), geometry=geom).get('ozone')
    
  def ozone_fill(geom,O3_date,fill):
    
    jan01 = ee.Date.fromYMD(O3_date.get('year'),1,1)
    doy_index = date.difference(jan01,'day').toInt()#.add(1) (i.e. index is one less than doy)
    fill_image = ee.Image(fill.get(doy_index))
    return fill_image.reduceRegion(reducer=ee.Reducer.mean(), geometry=geom).get('ozone')
   
  # O3 datetime in 24 hour intervals
  O3_date = round_date(date,24)
  
  # fix TOMS temporal gap
  TOMS_gap = ee.DateRange('1994-11-01','1996-08-01')  
  ozone = ee.Algorithms.If(TOMS_gap.contains(O3_date),ozone_fill(geom,O3_date,fill),ozone_measurement(geom,O3_date))

  # fix spatial gaps
  ozone = ee.Algorithms.If(ozone,ozone,ozone_fill(geom,O3_date,fill))
  
  #convert to Py6S units 
  ozone_Py6S_units = ee.Number(ozone).divide(1000)# (i.e. Dobson units are milli-atm-cm )                             
  
  return ozone_Py6S_units

