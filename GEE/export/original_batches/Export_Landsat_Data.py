# -*- coding: utf-8 -*-
"""
A copy of the python module used to export the Landsat data archive
(original name: 'export_landsat_v3.py)
"""

##EXPORT LANDSAT GEOTIFFs

#initialize Python
python

#initialize Earth Engine
import ee, time
ee.Initialize()

#target information
target_fc = ee.FeatureCollection('ft:1TfIROVmHbDIRCL18mjd3H4g40LxEDe-qgqocilWy').sort('volcano')
num_targets = target_fc.size().getInfo()

#batch process all targets in one go
list = target_fc.toList(200)
for i in range(98,103):#num_targets
  #target name
  target_name = str(ee.Feature(list.get(i)).get('volcano').getInfo())
  print(target_name)
  
  #geometries
  targetGeom = ee.FeatureCollection('ft:12PQq9qXwrGs_GOwaL8XtNvYEPnbhW7ercpiIFv0h')\
    .filter(ee.Filter.equals('name', target_name))\
    .geometry()
  subsetGeom = ee.FeatureCollection('ft:1tTg2YjXCY5eytm8p33a5NRAnKCeA5U-TtsbXBHEl')\
    .filter(ee.Filter.equals('name', target_name))\
    .geometry()
  # python subset geometry work around (convert to string)
  subsetGeomString = (subsetGeom.getInfo())[u'coordinates']
  
  #batch process all missions in one go
  missions = ['Landsat4','Landsat5','Landsat7','Landsat8']
  for j in range (0,4):
    mission = missions[j]
        
    #satelite mission variables
    if mission == 'Landsat4':
      imageCollectionID = 'LANDSAT/LT4_L1T'
      VSWIR_bands = ['B1','B2','B3','B4','B5','B7']
      TIR_bands = ['B6']
      TIR_scale = 120
    
    if mission == 'Landsat5':
      imageCollectionID = 'LANDSAT/LT5_L1T'
      VSWIR_bands = ['B1','B2','B3','B4','B5','B7']
      TIR_bands = ['B6']
      TIR_scale = 120 
    
    if mission == 'Landsat7':
      imageCollectionID = 'LANDSAT/LE7_L1T'
      VSWIR_bands = ['B1','B2','B3','B4','B5','B7']
      TIR_bands = ['B6_VCID_1','B6_VCID_2']
      TIR_scale = 60 
    
    if mission == 'Landsat8':
      imageCollectionID = 'LANDSAT/LC8_L1T'
      VSWIR_bands = ['B2','B3','B4','B5','B6','B7']
      TIR_bands = ['B10','B11']
      TIR_scale = 100 
       
    #DN to radiance function
    def DN_to_rad(img): return ee.Algorithms.Landsat.calibratedRadiance(img)
    
    ##image collection
    ic = ee.ImageCollection(imageCollectionID)\
      .filterBounds(targetGeom)\
      .map(DN_to_rad)
    
    #check scenes exist
    count = ic.size().getInfo()
    if count >= 0: 
      #export loop
      for k in range(0,count):
      # report progress
        print(mission+' '+target_name+': '+str(k+1)+' of '+str(count))
      # define images
        img = ee.Image(ic.toList(1, k).get(0))
        VSWIR = img.select(VSWIR_bands)
        TIR = img.select(TIR_bands)
      # define filename
        filename = ee.String(img.get("system:index")).getInfo()
      # define download export tasks
        VSWIR_task = ee.batch.Export.image(VSWIR.unmask(-9999), filename+'_VSWIR',\
        {'driveFolder':'LANDSAT_'+target_name,'scale':30,'region':subsetGeomString})
        TIR_task   = ee.batch.Export.image(TIR.unmask(-9999),filename+'_TIR',\
        {'driveFolder':'LANDSAT_'+target_name,'scale':TIR_scale,'region':subsetGeomString})
      # run export task
        VSWIR_task.start()
        TIR_task.start()



