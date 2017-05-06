#!/home/sam/anaconda3/bin/python
import sys
import ee
import datetime
import time

def geometry(target):
  switch = {
    'Kelimutu':ee.Geometry.Rectangle(121.80044, -8.77643,121.82782, -8.75429),
    'Ijen':ee.Geometry.Rectangle(114.22082, -8.07631, 114.26348, -8.04011)
  }
  return switch[target]

"""
Use an enclosure to pass geom to the mapping function which will be named
'RGB_extractor'
"""
def enclose_geom(geom):

  def mapping_function(img):
    """
    returns an RGB visualization of an image (timestamped)
    """

    img = ee.Image(img)
    rgb = img.clip(geom).visualize(min = 0, max = 0.4) 
    timestamp = ee.Number(img.get('system:time_start')).divide(1000)
    
    return rgb.set('timestamp',timestamp)

  return mapping_function

def RGB_list(geom):
  """
  Creates list of RGB visualizations for all available Landsat images of target geometry
  """

  # image collections
  L4 = ee.ImageCollection('LANDSAT/LT4_L1T_TOA').select(['B3','B2','B1']).filterDate('1980-01-01', '2017-01-01').filterBounds(geom.centroid())
  L5 = ee.ImageCollection('LANDSAT/LT5_L1T_TOA').select(['B3','B2','B1']).filterDate('1980-01-01', '2017-01-01').filterBounds(geom.centroid())
  L7 = ee.ImageCollection('LANDSAT/LE7_L1T_TOA').select(['B3','B2','B1']).filterDate('1980-01-01', '2017-01-01').filterBounds(geom.centroid())
  L8 = ee.ImageCollection('LANDSAT/LC8_L1T_TOA').select(['B4','B3','B2']).filterDate('1980-01-01', '2017-01-01').filterBounds(geom.centroid())
  merged = L4.merge(L5).merge(L7).merge(L8)
  
  ##!!////////////////////////////
  merged = L5
  ##!!////////////////////////////

  # RGB extractor (i.e. mapping function with enclosed geom)
  RGB_extractor = enclose_geom(geom)

  return merged.map(RGB_extractor).toList(1000)

def main():

  args = sys.argv[1:]
  if not args:
    print('usage: $ python3 export_LANDSAT_visualizations.py {target}')
    return
  target = args.pop(0)

  # start Earth Engine
  ee.Initialize()
    
  # geometry
  geom = geometry(target)

  # RGB list
  RGBs = RGB_list(geom)

  # RGB list size
  num = RGBs.length().getInfo()
  print(num)
  # export list elements
  for i in range(num):
    
    # this rgb visual
    rgb = ee.Image(RGBs.get(i))

    # filename from datetime
    timestamp = rgb.get('timestamp').getInfo()
    date = datetime.datetime.utcfromtimestamp(timestamp)
    filename = target+'_'+date.strftime('%Y_%m_%d_%H%M')
    
    # export
    task = ee.batch.Export.image.toDrive(image=rgb,
                                        description= filename,
                                        folder = '',
                                        scale = 30,
                                        dimensions = 400)
    task.start() 

    print('Progress = {0} of {1}, fileID = {2}'.format(i+1,num,filename))
    
    # take naps
    # nap = 240
    # print('sleeping for {} secs..'.format(nap))
    # time.sleep(nap) # <-------------------------------------------------------------------------- sleeper

if __name__ == '__main__':
  main()