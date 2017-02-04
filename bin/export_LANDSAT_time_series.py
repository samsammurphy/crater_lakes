"""
export_LANDSAT_time_series.py, Sam Murphy (2016-10-26)

2017-01-10: updated to be more inline with export_ASTER_time_series.py

This is a Google Earth Engine task manager. It sends lake data to a 
Google Drive folder called 'Ldata_{target}'

OUTPUT
-------------------------------------------------------------------------------
- radiance (visible, nir, swir and tir)
- lake pixel count
- thermal infrared brightness temperature
- water vapour and ozone
- LEDAPS surface reflectance (where available)

"""
import ee
import preprocess_LANDSAT
from masks import Mask
from lake_analyses import LakeAnalysis
from atmospheric import Atmospheric
from LEDAPS import Ledaps


def color_metrics(toa):
    """
    Calculates 
    
    - (new) 2D 'saturation' and 'value' of red-green space, and
    - (traditional) 3D Hue-Saturation-Value IF blue band available.
    
    """
    
    # 2D color: ASTER & LANDSAT
    R = ee.Image(toa).select(['red'])
    G = ee.Image(toa).select(['green'])
    saturation = R.subtract(G).abs()
    value = R.max(G)
    metrics = ee.Dictionary({'2D':
                                ee.Dictionary({'saturation':saturation,'value':value})
                            })
    
    # 3D color: LANDSAT only
    hasBlue = ee.List(ee.Image(toa).bandNames()).contains('blue')
    HSV = ee.Algorithms.If(hasBlue,\
      ee.Image(toa).select(['red','green','blue']).rgbToHsv(),'null')
    metrics = ee.Dictionary(metrics).set('3D',HSV)
        
    return metrics
    
def brightnessTemperature(toa):
  
  BT = ee.Image(ee.Dictionary(toa).get('tir')).select('tir1') 

  return BT

    
# extracts data from an image (will be mapped over collection)
def extraction(geom):
  """
  A closure to hold target geometry when mapped over image collection
  """
  
  def extract_data(img):
    """
    Preprocesses scenes, applies masks, extracts radiance data and pixel counts
    """
     
    # preprocessing
    rad = preprocess_LANDSAT.toRad(img) # at-sensor radiance
    toa = preprocess_LANDSAT.toToa(img) # top of atmosphere reflectance
    BT  = brightnessTemperature(toa)
     
    # vnir color metrics
    color = color_metrics(toa.get('vnir'))
       
    # cloud mask
    cloud = Mask.cloud(color, BT)
    
    # water mask
    water = Mask.water(toa.get('vnir')) 
       
    # lake analyses
    vnir = LakeAnalysis.vnir(rad,geom,cloud,water,BT)
    swir = LakeAnalysis.swir(rad,geom,cloud,water,BT)
    tir = LakeAnalysis.tir(rad,geom,cloud,water)
      
    # date and time
    date = ee.Date(img.get('system:time_start'))
    jan01 = ee.Date.fromYMD(date.get('year'),1,1)
    doy = date.difference(jan01,'day').add(1)
      
    data = ee.Dictionary({
                            'date':date,
                            'doy':doy,
                            'vnir':vnir,
                            'swir':swir,
                            'tir':tir,
                            'solar_z':ee.Number(90.0).subtract(img.get('SUN_ELEVATION')),
                            'H2O':Atmospheric.water(geom,date),
                            'O3':Atmospheric.ozone(geom,date),
                            'LEDAPS':ee.Dictionary(Ledaps.find(img,date,geom))
                            })
  
    return ee.Feature(geom,data)
  return extract_data
  
def LANDSAT_export(target):

  # start Earth Engine
  ee.Initialize()
  
#  target = 'Ruapehu'
  
  # geometry (crater box)
  geom = ee.FeatureCollection('ft:1hReJyYMkes0MO2Kgl6zTsKPjruTimSfRSWqQ1dgF')\
    .filter(ee.Filter.equals('name', target)).geometry();
  
  # image collections
  ics = ({\
    'L4':ee.ImageCollection('LANDSAT/LT4_L1T').filterBounds(geom).filterDate('1900-01-01','2016-01-01'),\
    'L5':ee.ImageCollection('LANDSAT/LT5_L1T').filterBounds(geom).filterDate('1900-01-01','2016-01-01'),\
    'L7':ee.ImageCollection('LANDSAT/LE7_L1T').filterBounds(geom).filterDate('1900-01-01','2016-01-01'),\
    'L8':ee.ImageCollection('LANDSAT/LC8_L1T').filterBounds(geom).filterDate('1900-01-01','2016-01-01')
  })
  
  # satellite missions
  sats = ['L4','L5','L7','L8']
  
  for sat in sats:
      
    #image collection
    ic = ics[sat]
    
    # image collection size
    print(sat+' count = ',ic.aggregate_count('system:index').getInfo())
    
    # mapping function closure
    extract_data = extraction(geom)
    
    # feature collection of results
    data = ic.map(extract_data)
    
    # export to table
    ee.batch.Export.table.toDrive(collection = data,\
                                  description = sat+'_'+target,\
                                  folder = 'Ldata_'+target,\
                                  fileFormat= 'GeoJSON'\
                                  ).start()

#
#if __name__ == '__main__':
#  main()








