#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

export_hack.py

Created on Sat Feb  4 09:31:39 2017

@author: sam
"""

from export_ASTER_time_series import ASTER_export
from export_LANDSAT_time_series import LANDSAT_export


volcano_name = 'Kelimutu_c'
ASTER_export(volcano_name)
LANDSAT_export(volcano_name)