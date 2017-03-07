import ee
import datetime

# start Earth Engine
ee.Initialize()
  
# geometry of image outline
geom = ee.Geometry.Rectangle(121.80044, -8.77643,121.82782, -8.75429)
geomString = (geom.getInfo())[u'coordinates']# python work around (i.e. convert to string)

# image collection
L4 = ee.ImageCollection('LANDSAT/LT4_L1T_TOA').select(['B3','B2','B1']).filterDate('1900-01-01', '2016-01-01').filterBounds(geom.centroid())
L5 = ee.ImageCollection('LANDSAT/LT5_L1T_TOA').select(['B3','B2','B1']).filterDate('1900-01-01', '2016-01-01').filterBounds(geom.centroid())
L7 = ee.ImageCollection('LANDSAT/LE7_L1T_TOA').select(['B3','B2','B1']).filterDate('1900-01-01', '2016-01-01').filterBounds(geom.centroid())
L8 = ee.ImageCollection('LANDSAT/LC8_L1T_TOA').select(['B4','B3','B2']).filterDate('1900-01-01', '2016-01-01').filterBounds(geom.centroid())
LANDSAT = L4.merge(L5).merge(L7).merge(L8)

# list
image_list = LANDSAT.toList(1000)
num = image_list.length().getInfo()

# loop list
for i in range(5,100):
    
  # visualize kelimutu
  img = ee.Image(image_list.get(i))
  rgb = img.clip(geom).visualize(min = 0, max = 0.4) 
  
  # filename from datetime
  timestamp = img.get('system:time_start').getInfo() / 1000
  date = datetime.datetime.utcfromtimestamp(timestamp)
  filename = date.strftime('%Y_%m_%d_%H%M')
  
  print('Progress = {0} of {1}, fileID = {2}'.format(i+1,num,filename))

  # export
  task = ee.batch.Export.image.toDrive(image=rgb,\
                                       description=filename,\
                                       folder = 'Kelimutu_RGBs',
                                       scale = 30,
                                       dimensions = 400)
  task.start() 
