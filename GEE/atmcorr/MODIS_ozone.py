# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 15:19:35 2016

@author: sam
"""

import ee
ee.Initialize()

ic = ee.ImageCollection('MODIS/MOD08_M3_051')
img = ee.Image(ic.first())

print(img.select('Total_Ozone_Mean_Mean'))

#Total_Ozone_Mean_Mean
#Total_Ozone_Std_Deviation_Mean
#Total_Ozone_QA_Mean_Mean
#Total_Ozone_QA_Std_Deviation_Mean
