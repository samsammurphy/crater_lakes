"""
Exports the mean of the mean for doys between
1) 1980-1994
2) 1997-2016

The general idea is to avoid the TOMS hiatus and provide an improved interpolation
scheme over that offered by USGS

The time periods run from AND TO January 1st, i.e. only 1st day of 1994 and 2016 are included
"""

import numpy as np
import ee
ee.Initialize()

#time periods
older = 'users/samsammurphy/ozone_mean_doy_1980-1994/'
newer = 'users/samsammurphy/ozone_mean_doy_1997-2016/'

#georeference
crs = 'EPSG:4326'
crsTransform = [1.25, 0.0, -180.0, 0.0, -1.0, 90.0]
region = [[-180.0, 90.0], [-180.0, -90.0], [180.0, -90.0], [180.0, 90.0], [-180.0, 90.0]]

# days of the year
doys = list(np.linspace(2,365,364))
for doy in doys:

  #image name for this day of year
  image_name = 'ozone_'+str(int(doy)).zfill(3)
  
  #mean ozones (i.e. for each period)
  meanOzone1 = ee.Image(older+image_name)
  meanOzone2 = ee.Image(newer+image_name)
  
  # mean mean ozone (i.e. of both periods together)
  meanmean = ee.Image(meanOzone1.add(meanOzone2).divide(2)) \
    .set('doy',doy).reproject(crs,crsTransform)
    
  # asset ID
  assetID = 'users/samsammurphy/ozone_mean_doy/'+image_name
  
  # export task
  task = ee.batch.Export.image.toAsset(\
      image=meanmean,
      description='meanmean ozone export of '+image_name,
      assetId=assetID,
      region=region, 
      # if not specified, region defaults to the viewport at the time of invocation. 
      # i.e. if viewport not specified the image is unbound (which raises an error)
      crs=crs, 
      crsTransform=crsTransform
      )
  
  # start the export task
  task.start()
