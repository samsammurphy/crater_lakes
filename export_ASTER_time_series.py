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
from lake_analyses import LakeAnalysis
from atmospheric import get_water_vapour
from atmospheric import get_ozone



def color_metrics(toa):
  """
  Calculates 
  
  - (new) 2D 'saturation' and 'value' of red-green space
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

def cloud_mask(color, BT):
  """
  Cloud pixels are grey, bright and cold
  
  - grey and bright: 2D Saturation and Value
  - cold: Brightness Temperature
  
  More detail on grey and bright threshold:
  - Saturation always < 0.1
  - if Value between 0.1 and 0.2 then Saturation must be 0.1 less than Value
  - Value always > 0.1 (i.e. negative Saturation not possible)
  """
  
  # 2D saturation and value
  color2D = ee.Dictionary(ee.Dictionary(color).get('2D'))
  saturation = ee.Image(color2D.get('saturation'))
  value = ee.Image(color2D.get('value'))
  
  # saturation threshold (based on value)
  # threshold = value.subtract(0.1).updateMask(value.lte(0.2)).unmask(0.1,False)   <- original
  threshold = value.subtract(0.15).updateMask(value.lt(0.3)).unmask(0.15,False)     

  # cloud pixels
  grey_and_bright = saturation.lt(ee.Image(threshold))
  cold = ee.Image(BT).lt(20)
  cloud = grey_and_bright.multiply(cold)
  
  # clouds are nebulous, fluffy edges are included (100m radius)
  cloudy = cloud.distance(ee.Kernel.euclidean(100, "meters")).gte(0).unmask(0, False)

  return cloudy.rename(['cloud'])
  
def water_mask(toa):
  """
  Water pixels have an NDWI > 0.3 (Normalized Difference Water Index)
  """
  
  ndwi = ee.Image(toa).normalizedDifference(['green','nir'])
  water = ndwi.gte(0.1)

  return water.rename(['water'])  
 
# extracts data from an image (will be mapped over collection)
def extraction(geom):
  """
  A closure to hold target geometry when mapping over image colleciton
  """
  
  def extract_data(img):
     
    # preprocessing
    rad = Aster.radiance.fromDN(img)     # at-sensor radiance
    toa = Aster.reflectance.fromRad(rad) # top of atmosphere reflectance
    BT  = Aster.temperature.fromRad(rad) # brightness temperature
    
    # Brightness temperature of just band 14 (11.3 micron) 
    BT14 = ee.Image(BT).select('BT14')
     
    # color metrics
    color = color_metrics(toa.get('vnir'))
  
    # cloud mask
    cloud = cloud_mask(color, BT14)
    
    # water mask
    water = water_mask(toa.get('vnir')) 
  
    # lake analyses
    vnir = LakeAnalysis.vnir(rad,geom,cloud,water)
    swir = LakeAnalysis.swir(rad,geom,cloud,water)
    tir = LakeAnalysis.tir(rad,geom,cloud,water)
    
    # date and time
    date = ee.Date(img.get('system:time_start'))
    jan01 = ee.Date.fromYMD(eeDate.get('year'),1,1)
    doy = eeDate.difference(jan01,'day').add(1)
  
    result = ee.Dictionary({
                            'date':date,
                            'doy':doy,
                            'vnir':vnir,
                            'swir':swir,
                            'tir':tir,
                            'solar_z':ee.Number(90.0).subtract(img.get('SOLAR_ELEVATION')),
                            'H2O':get_water_vapour(geom,date),
                            'O3':get_ozone(geom,date)
                            })

    return ee.Feature(geom,result)
    
  return extract_data
  
  
def main():
  
  # start Earth Engine
  ee.Initialize()
  
  # target lake  
  target = 'Kelut'
 
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
  print('count = ',aster.aggregate_count('system:index').getInfo())
  
  # mapping function
  extract_data = extraction(geom)
  
  # feature collection of results
  data = aster.map(extract_data)
    
  ee.batch.Export.table.toDrive(data, 'AST_'+target,'Ldata_'+target).start()

if __name__ == '__main__':
  main()
