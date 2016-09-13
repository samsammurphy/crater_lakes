"""


WARNING!!!
Exporting to image collection is not possible (apparently)


Idea was to:
Creates an image collection from the mean ozone images and export to asset

"""

import numpy as np
import ee
ee.Initialize()



# image list
image_list = []
doys = list(np.linspace(1,50,50,dtype=np.int))
for doy in doys:
  assetID = 'users/samsammurphy/ozone_images/ozone_'+str(doy).zfill(3)
  ozone = ee.Image(assetID)
  image_list.append(ozone)

# image list to collection
ozone_doy_mean = ee.ImageCollection.fromImages(image_list)
#print(ozone_doy_mean.getInfo())  # it worked


