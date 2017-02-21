"""
export_ASTER_time_series.py, Sam Murphy (2017-01-02)

This is a Google Earth Engine task manager. It sends lake data to a 
Google Drive folder called 'Ldata_{target}'

OUTPUT
-------------------------------------------------------------------------------
- radiance (visible, nir, swir and tir)
- lake pixel count
- thermal infrared brightness temperature
- water vapour and ozone

NOTE
-------------------------------------------------------------------------------
ASTER processing is separated from Landsat due to differences in operational
functionality of these missions. ASTER has separate subsystems which can be
on/off and have dynamic gain coefficients.
"""

import ee
from preprocess_ASTER import Aster
from masks import Mask
from lake_analyses import LakeAnalysis
from atmospheric import Atmospheric


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
    
    # 3D color
    hasBlue = ee.List(ee.Image(toa).bandNames()).contains('blue')
    HSV = ee.Algorithms.If(hasBlue,\
      ee.Image(toa).select(['red','green','blue']).rgbToHsv(),'null')
    metrics = ee.Dictionary(metrics).set('3D',HSV)
        
    return metrics
    
def brightnessTemperature(rad):
  
  BTs = Aster.temperature.fromRad(rad)# all BTs (for each TIR waveband)
  BT14 = ee.Image(BTs).select('BT14') # just band 14 (11.3 microns) 
  
  return(BT14)
  
 
# extracts data from an image (will be mapped over collection)
def extraction(geom):
  """
  A closure to hold target geometry when mapped over image colleciton
  """
  
  def extract_data(img):
    """
    Preprocesses scenes, applies masks, extracts radiance data and pixel counts
    """
     
    # preprocessing
    rad = Aster.radiance.fromDN(img)     # at-sensor radiance
    toa = Aster.reflectance.fromRad(rad) # top of atmosphere reflectance
    BT  = brightnessTemperature(rad)     # brightness temperature, single band
    
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
  
    result = ee.Dictionary({
                            'date':date,
                            'doy':doy,
                            'vnir':vnir,
                            'swir':swir,
                            'tir':tir,
                            'solar_z':ee.Number(90.0).subtract(img.get('SOLAR_ELEVATION')),
                            'H2O':Atmospheric.water(geom,date),
                            'O3':Atmospheric.ozone(geom,date),
                            'AOT':Atmospheric.aerosol(geom,date)
                            })

    return ee.Feature(geom,result)
    
  return extract_data
  
  
def ASTER_export(target):
  
  # start Earth Engine
  ee.Initialize()
  
#  # target lake  
#  target = 'Kelut'
 
  # geometry (crater outline)
  geom = ee.FeatureCollection('ft:1hReJyYMkes0MO2Kgl6zTsKPjruTimSfRSWqQ1dgF')\
    .filter(ee.Filter.equals('name', target))\
    .geometry()
  
  # image collection
  aster = ee.ImageCollection('ASTER/AST_L1T_003')\
    .filterBounds(geom.centroid())\
    .filterDate('1900-01-01','2016-01-01')\
    .filter(ee.Filter.And(\
      ee.Filter.listContains('ORIGINAL_BANDS_PRESENT', 'B01'),\
      ee.Filter.listContains('ORIGINAL_BANDS_PRESENT', 'B10')\
      ))
    #.filterMetadata('system:index','equals','20080506231313')
      
  # image collection size
  print('ASTER = ',aster.aggregate_count('system:index').getInfo())
  
  # mapping function
  extract_data = extraction(geom)
  
  # feature collection of results
  data = aster.map(extract_data)
  
  # export to table
  ee.batch.Export.table.toDrive(collection = data,\
                                description = 'AST_'+target,\
                                folder = 'LakeData_'+target,\
                                fileFormat= 'GeoJSON'\
                                ).start()

#if __name__ == '__main__':
#  main()
