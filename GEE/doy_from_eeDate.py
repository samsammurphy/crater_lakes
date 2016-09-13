import ee

def doy_from_eeDate(eeDate):
  """
  day-of-year (i.e. used in harmonic correction for earth's elliptical orbit)
  """
  jan01 = ee.Date.fromYMD(eeDate.get('year'),1,1)
  doy = eeDate.difference(jan01,'day').add(1)
  return doy