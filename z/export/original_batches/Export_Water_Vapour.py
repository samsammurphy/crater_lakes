# -*- coding: utf-8 -*-
"""
Atmospheric water vapour column over a volcano through time (kg/m2)

Export to a .CSV file in Google Drive

Created on Thu Apr 28 05:54:08 2016

@author: sam
"""

#Google Earth Engine
import ee
ee.Initialize()

#targets
target_fc = ee.FeatureCollection('ft:12PQq9qXwrGs_GOwaL8XtNvYEPnbhW7ercpiIFv0h').sort('volcano')
num_targets = target_fc.size().getInfo()

#batch process all targets in one go
list = target_fc.toList(200)
for i in range(0,num_targets):#num_targets
  
  #target name
  target_name = str(ee.Feature(list.get(i)).get('name').getInfo())
  print(target_name)

  #centroid of crater lake box
  geom = ee.FeatureCollection('ft:12PQq9qXwrGs_GOwaL8XtNvYEPnbhW7ercpiIFv0h').filter(ee.Filter.equals('name', target_name)).geometry().centroid()
  
  #image collection
  water_ic = ee.ImageCollection('NCEP_RE/surface_wv').filterBounds(geom).filterDate('1980-01-01','2016-01-01')
  
  #georegistration dictionary
  img = ee.Image(water_ic.first())
  crs = img.projection().crs()
  scale = img.projection().nominalScale()
  
  #function to extract water vapour column above the volcano
  def extract_water(img):
    
    water = img.reduceRegion(ee.Reducer.mean(),geom,scale,crs)
    
    #return a feature
    H2Odict = {}                        #Water vapour dictionary (i.e. to put value into a feauture)
    H2Odict['H2O'] = ee.Number(water)    #assign water value to dictionary
    feature = ee.Feature(None, H2Odict) #feature = geom + dictionary (by definition)  <-- update: used null geom for smaller output file
    return feature                      #mapped functions can only return images or features
  
  #extract water vapour column for each image in collection
  water_fc = water_ic.map(extract_water)
  
  #define export task
  taskDic = {}
  taskDic['fileFormat'] = 'CSV'
  taskDic['driveFolder'] = 'water_vapour'
  task = ee.batch.Export.table(water_fc, target_name, taskDic)
  
  # run export task
  task.start()

