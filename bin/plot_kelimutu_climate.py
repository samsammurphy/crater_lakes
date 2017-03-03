#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

plot_kelimutu_climate.py

Created on Thu Mar  2 17:29:02 2017
@author: sam
"""


import glob
#import re

# open climate file 
bpath = '/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/data/Kelimutu/climate/'
fpaths = sorted(glob.glob(bpath+'Met*.txt'))
file = open(fpaths[0])

# read file to list 
lines = file.readlines()

# header
header = lines.pop(0).split()

# read data columns
