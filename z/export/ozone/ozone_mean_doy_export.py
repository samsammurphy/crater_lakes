"""

OZONE FILL

Calculates the mean ozone value for a given day of year within a given time 
period and exports to Google Earth Engine.

N.B. Downloading as geotiff is possible if desired, i.e. use the .toDrive() 
method of 'ee.batch.Export.image' instead of .toAsset()

"""

import ee
import numpy as np

# initialize Google EarthEngine
ee.Initialize()

# time period
startDate = ee.Date('1980-01-01')
stopDate = ee.Date('1994-01-01')

# adds day-of-year to image collection
def doy(img):
  d = ee.Date(img.get('system:time_start'))
  jan01 = ee.Date.fromYMD(d.get('year'),1,1)
  doy = d.difference(jan01,'day').add(1)
  return img.set('doy',doy)

# ozone collection (with day of year)
ozone_ic = ee.ImageCollection('TOMS/MERGED')\
  .filterDate(startDate,stopDate)\
  .map(doy)
  
# georeference information (for export)
info = ee.Image(ozone_ic.first()).getInfo()
crs = info['bands'][0]['crs']
crsTransform = info['bands'][0]['crs_transform']
region = [[-180.0, 90.0], [-180.0, -90.0], [180.0, -90.0], [180.0, 90.0], [-180.0, 90.0]]

# days of the year
doys = list(np.linspace(1,366,366))

for doy in doys:

  doy_ic = ozone_ic.filter(ee.Filter.eq('doy', doy))
  
  # mean ozone for this day-of-year
  doy_mean = doy_ic.mean().set('doy',doy).reproject(crs,crsTransform)
  
  # asset ID
  assetID = 'users/samsammurphy/ozone_mean_doy_1980-1994/ozone_'+str(int(doy)).zfill(3)
  
  # export task
  task = ee.batch.Export.image.toAsset(\
      image=doy_mean,
      description='ozone export for doy '+str(int(doy)),
      assetId=assetID,
      region=region, 
      # if not specified, region defaults to the viewport at the time of invocation. 
      # i.e. if viewport not specified the image is unbound (which raises an error)
      crs=crs, 
      crsTransform=crsTransform
      )
  
  # start the export task
  task.start()
