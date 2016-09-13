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

def get_ozone(geom,date):
  
  # O3 datetime is in 24 hour intervals
  O3_date = round_date(date,24)
  
  #TODO test if the date is within the TOMS gap
  # if yes (then use a mean value)
  # if no (then try to find a contemporary value)
  
  #filtered ozone collection
  ozone_ic = ee.ImageCollection('TOMS/MERGED').filterDate(O3_date)
  
  #ozone image
  ozone_img = ee.Image(ozone_ic.first())
  
  #ozone column over target
  ozone = ozone_img.reduceRegion(reducer=ee.Reducer.mean(), geometry=geom).get('ozone').getInfo()
  
  #TODO test if the contemporary value is a number
  # if yes, great
  # if no, then use a mean value
#  test = ee.Algorithms.If(ozone==None,'use_mean_value','value_found')
#  print(test.getInfo())
#  print(ozone)
  
  return ozone

##  if ozone.getInfo() == None:
##    ozone = get_ozone_estimate()
#
##convert to Py6S units (Google = Dobson Units, Py6S = atm-cm)
#ozone_Py6S_units = ee.Number(ozone).divide(1000)# (i.e. Dobson units are milli-atm-cm )                             
#
#print(ozone_Py6S_units.getInfo())

geom = ee.Geometry.Point(0,0)
date = ee.Date('2000-01-01').advance(3,'hour')
ozone = get_ozone(geom,date)