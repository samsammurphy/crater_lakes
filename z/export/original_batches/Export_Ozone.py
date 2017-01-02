# -*- coding: utf-8 -*-
"""
Atmospheric ozone column at a volcano through time (in Dobson Units)

Dobson units (DU)
----------------------
1 DU = 2.1414e-2 g/m2
1 DU = 2.1414e-5 kg/m2
1 DU = 2.1414e-6 g/cm2

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
  ozone_ic = ee.ImageCollection('TOMS/MERGED').filterBounds(geom).filterDate('1980-01-01','2016-01-01')
  
  #georegistration dictionary
  img = ee.Image(ozone_ic.first())
  crs = img.projection().crs()
  scale = img.projection().nominalScale()
  
  #function to extract ozone column above the volcano
  def extract_ozone(img):
    
    ozone = img.reduceRegion(ee.Reducer.mean(),geom,scale,crs)
    
    #return a feature
    O3dict = {}                        #Ozone dictionary (i.e. to put value into a feauture)
    O3dict['O3'] = ee.Number(ozone)    #assign ozone value to dictionary
    feature = ee.Feature(None, O3dict) #feature = geom + dictionary (by definition)  <-- update: used null geom for smaller output file
    return feature                     #mapped functions can only return images or features
  
  #extract ozone column for each image in collection
  ozone_fc = ozone_ic.map(extract_ozone)
  
  #define export task
  taskDic = {}
  taskDic['fileFormat'] = 'CSV'
  taskDic['driveFolder'] = 'ozone'
  task = ee.batch.Export.table(ozone_fc, target_name, taskDic)
  
  # run export task
  task.start()

