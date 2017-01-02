import numpy as np
import ee
ee.Initialize()

# georeference
crs = 'EPSG:4326'
crsTransform = [1.25, 0.0, -180.0, 0.0, -1.0, 90.0]
region = [[-180.0, 90.0], [-180.0, -90.0], [180.0, -90.0], [180.0, 90.0], [-180.0, 90.0]]

doys = list(np.linspace(101,366,266))
for doy in doys:
  image_assetID = 'users/samsammurphy/ozone_mean_doy/ozone_'+str(int(doy)).zfill(3)
  imageCollection_assetID = 'users/samsammurphy/public/ozone_fill/ozone_'+str(int(doy)).zfill(3)
  ozone_img = ee.Image(image_assetID)

  # export task
  task = ee.batch.Export.image.toAsset(\
      image=ozone_img,
      description='add to image collection: ozone_'+str(int(doy)).zfill(3),
      assetId=imageCollection_assetID,
      region=region, 
      crs=crs, 
      crsTransform=crsTransform
      ).start()