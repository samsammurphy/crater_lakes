# -*- coding: utf-8 -*-
"""
preprocess.py, Sam Murphy (2016-10-24)

Basic preprocessing of ASTER imagery (i.e. spectral subsets, renames bands,
convert from DN to radiance/TOA/BT)

Things to note

1) ASTER gain coefficients are dynamic for VNIR and SWIR subsystems (i.e. they
can be high, normal, low1 and low2)

2) ASTER subsystems can be on/off. Explicitly tested for here.
"""

import ee
import math

class Aster():
  
  class radiance():
    
    def fromDN(image):
      
      def subsystemsOn(image):
        """
        check which subsystems are on/off
        """
        
        ic = ee.ImageCollection(image)# create image collection for filtering
      
        vnir_on = ic.filter(ee.Filter.listContains('ORIGINAL_BANDS_PRESENT','B01')).aggregate_count('system:index')
        swir_on = ic.filter(ee.Filter.listContains('ORIGINAL_BANDS_PRESENT','B04')).aggregate_count('system:index')
        tir_on  = ic.filter(ee.Filter.listContains('ORIGINAL_BANDS_PRESENT','B10')).aggregate_count('system:index')
        
        return [vnir_on, swir_on, tir_on]
        
      def vnirRad(image):
        """
        Radiance from visible through near-infrared (VNIR) subsystem
        """

        VNIR_gains = ee.Image([\
        ee.Number(image.get('GAIN_COEFFICIENT_B01')).float(),\
        ee.Number(image.get('GAIN_COEFFICIENT_B02')).float(),\
        ee.Number(image.get('GAIN_COEFFICIENT_B3N')).float()\
        ])
        
        vnir = image.select(['B01','B02','B3N'],['green','red','nir'])\
                    .subtract(1).multiply(VNIR_gains)
        
        return vnir
        
      def swirRad(image):
        """
        Radiance from short-wave infrared (SWIR) subsytem
        """
        
        SWIR_gains = ee.Image([\
        ee.Number(image.get('GAIN_COEFFICIENT_B04')).float(),\
        ee.Number(image.get('GAIN_COEFFICIENT_B05')).float(),\
        ee.Number(image.get('GAIN_COEFFICIENT_B06')).float(),\
        ee.Number(image.get('GAIN_COEFFICIENT_B07')).float(),\
        ee.Number(image.get('GAIN_COEFFICIENT_B08')).float(),\
        ee.Number(image.get('GAIN_COEFFICIENT_B09')).float()\
        ])
        
        swir =  image.select(['B04','B05','B06','B07','B08','B09'],\
                          ['swir1','swir2','swir3','swir4','swir5','swir6'])\
                          .subtract(1).multiply(SWIR_gains)
        
        return swir
      
      def tirRad(image):
        """
        Radiance from thermal Infrared (TIR) subsystem
        """
        
        TIR_gains = ee.Image([\
        ee.Number(image.get('GAIN_COEFFICIENT_B10')).float(),\
        ee.Number(image.get('GAIN_COEFFICIENT_B11')).float(),\
        ee.Number(image.get('GAIN_COEFFICIENT_B12')).float(),\
        ee.Number(image.get('GAIN_COEFFICIENT_B13')).float(),\
        ee.Number(image.get('GAIN_COEFFICIENT_B14')).float()\
        ])
        
        tir = image.select(['B10','B11','B12','B13','B14'],\
                          ['tir1','tir2','tir3','tir4','tir5'])\
                          .subtract(1).multiply(TIR_gains)
        
        return tir
     
      def getRadiance(image):
        """
        Checks subsystems and applies gain coefficients
        """
      
        subStates = subsystemsOn(image)
        
        vnir = ee.Algorithms.If(subStates[0],vnirRad(image),False)
        swir = ee.Algorithms.If(subStates[1],swirRad(image),False)
        tir  = ee.Algorithms.If(subStates[2],tirRad(image),False)
        
        # reflectance calculation requirements
        timeStamp = image.get('system:time_start')
        solar_z = ee.Number(90).subtract(image.get('SOLAR_ELEVATION'))
        
        radiance = ee.Dictionary({
                                  'vnir':vnir,
                                  'swir':swir,
                                  'tir':tir,
                                  'timeStamp':timeStamp,
                                  'solar_zenith':solar_z,
                                  'subsystem_states':subStates
                                  })
        
      
        return radiance
        
      return getRadiance(image)
              
  class temperature():
    
    def fromRad(radiance):
      """
      Calculates brightness temperature from radiance
      """
      
      def inversePlanck(tir):
        """
        Brightness temperatures using inverted Planck function
        """
                 
        k1 = ee.Image([3040.136402, 2482.375199, 1935.060183, 866.468575, 641.326517])
        k2 = ee.Image([1735.337945, 1666.398761, 1585.420044, 1350.069147, 1271.221673])
        
        temperature = k2.divide(k1.divide(tir).add(1).log())
        
        return temperature
      
      def getTemperature(radiance):

        tir = radiance.get('tir')
        temperature = ee.Algorithms.If(tir, inversePlanck(tir), False)
      
        return temperature
        
      return getTemperature(radiance)
  
  class reflectance():
    
    def fromRad(radiance):
      
      def rad2ref(radiance, multiplier, ESUN):
        """
        apply radiance to reflectance conversion
        
        'multiplier' is a scalar which accounts for Earth-Sun distance and angle
        'ESUN' is mean exoatospheric solar irradiance for subsystem's wavebands
        """
        
        step1 = ee.Image(radiance).multiply(ee.Number(multiplier))
        reflectance = step1.divide(ESUN)
      
        return reflectance
        
      def vnirRef(radiance, multiplier):
        """
        Reflectance for VNIR subsystem
        """
        
        vnirRad = radiance.get('vnir')
        ESUN = [1847,1553,1118]# from Thome et al (A) see http://www.pancroma.com/downloads/ASTER%20Temperature%20and%20Reflectance.pdf
        
        return rad2ref(vnirRad, multiplier, ESUN)
        
      def swirRef(radiance, multiplier):
        """
        Reflectance for SWIR subsystem
        """
        
        swirRad = radiance.get('swir')
        ESUN = [232.5,80.32,74.92,69.2,59.82,57.32]# from Thome et al (A) see http://www.pancroma.com/downloads/ASTER%20Temperature%20and%20Reflectance.pdf
        
        return rad2ref(swirRad, multiplier, ESUN)
        
      def getReflectance(radiance):
        """
        Calculates scalar multiplier, checks subsystems and applies radiance
        to reflectance conversion        
        """
        
        # Earth-Sun distance squared (d2) 
        date = ee.Date(radiance.get('timeStamp'))
        jan01 = ee.Date.fromYMD(date.get('year'),1,1)
        doy = date.difference(jan01,'day').add(1)
        d = ee.Number(doy).subtract(4).multiply(0.017202).cos().multiply(-0.01672).add(1) # http://physics.stackexchange.com/questions/177949/earth-sun-distance-on-a-given-day-of-the-year
        d2 = d.multiply(d)  
             
        # cosine of solar zenith angle (cosz)
        solar_z = ee.Number(radiance.get('solar_zenith'))
        cosz = solar_z.multiply(math.pi).divide(180).cos()
    
        # scalar multiplier (same for VNIR and SWIR)
        multiplier = ee.Number(math.pi).multiply(d2).divide(cosz)

        # apply correction
        subStates = ee.List(radiance.get('subsystem_states'))
        vnir = ee.Algorithms.If(subStates.get(0),vnirRef(radiance, multiplier),False)
        swir = ee.Algorithms.If(subStates.get(1),swirRef(radiance, multiplier),False)
        
        reflectance = ee.Dictionary({
                            'vnir':vnir,
                            'swir':swir,
                            'subsystem_states':subStates
                            })
        
        return reflectance
      
      return getReflectance(radiance)


