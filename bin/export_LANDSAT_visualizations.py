#!/home/sam/anaconda3/bin/python
import ee
import datetime
import time


# start Earth Engine
ee.Initialize()
  
# geometry of image outline
geom = ee.Geometry.Rectangle(121.80044, -8.77643,121.82782, -8.75429)
geomString = (geom.getInfo())[u'coordinates']# python work around (i.e. convert to string)

# mapper to get RGB visual with time stamp
def toRGB(img):
  
  img = ee.Image(img)
  rgb = img.clip(geom).visualize(min = 0, max = 0.4) 
  timestamp = ee.Number(img.get('system:time_start')).divide(1000)
  
  return rgb.set('timestamp',timestamp)

# image collections
L4 = ee.ImageCollection('LANDSAT/LT4_L1T_TOA').select(['B3','B2','B1']).filterDate('1900-01-01', '2016-01-01').filterBounds(geom.centroid())
L5 = ee.ImageCollection('LANDSAT/LT5_L1T_TOA').select(['B3','B2','B1']).filterDate('1900-01-01', '2016-01-01').filterBounds(geom.centroid())
L7 = ee.ImageCollection('LANDSAT/LE7_L1T_TOA').select(['B3','B2','B1']).filterDate('1900-01-01', '2016-01-01').filterBounds(geom.centroid())
L8 = ee.ImageCollection('LANDSAT/LC8_L1T_TOA').select(['B4','B3','B2']).filterDate('1900-01-01', '2016-01-01').filterBounds(geom.centroid())

# RGB list
RGB_list = L4.merge(L5).merge(L7).merge(L8).map(toRGB).toList(1000)

# RGB list size
num = RGB_list.length().getInfo()

# export list elements
for i in range(438,num):
   
  # this rgb visual
  rgb = ee.Image(RGB_list.get(i))

  # filename from datetime
  timestamp = rgb.get('timestamp').getInfo()
  date = datetime.datetime.utcfromtimestamp(timestamp)
  filename = date.strftime('%Y_%m_%d_%H%M')
  
  # export
  task = ee.batch.Export.image.toDrive(image=rgb,\
                                       description=filename,\
                                       folder = 'Kelimutu_RGBs',
                                       scale = 30,
                                       dimensions = 400)
  task.start() 

  print('Progress = {0} of {1}, fileID = {2}'.format(i+1,num,filename))

  print('sleeping for 90 secs..')
  time.sleep(90) # <-------------------------------------------------------------------------- sleeper
