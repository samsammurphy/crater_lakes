# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 13:39:07 2016

@author: sam
"""

import ee
ee.Initialize()

# spatial subset
top = -15.37325
bot = -15.40884
lef = 167.81118
rit = 167.86045
geom = ee.Geometry.Rectangle([lef, bot, rit, top]) # GEE geometry
JSON = [[[lef,bot],[lef,top],[rit,top],[rit,bot],[lef,bot]]] # JSON geometry

# at-senor radiance image collection 
collection = ee.ImageCollection('LANDSAT/LC8_L1T_TOA')\
.filterBounds(geom)\
.filterDate('2015-06-01', '2016-01-7')\
.select(['B5'])
  

# image example
img = collection.first()

# set up an export task
task = ee.batch.Export.image(img,'test7', {
'driveFolder':'quicky',
'scale':30,
'region':JSON
})

#export
task.start()

