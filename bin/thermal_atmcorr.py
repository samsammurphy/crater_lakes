#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

thermal_atmcorr.py

Created on Mon Feb  6 11:34:19 2017
@author: sam
"""

from physics import planck
#from surface_deltaTemperature import surface_deltaTemperature

def TIR_11micron(tir,satellite):
  """
  Returns 11 micron radiance (lake and bkgd) and central wavelength
  """
  
  # 11 micron radiance
  if satellite == 'AST':
    tir_11micron = 'tir5'
  else:
    tir_11micron = 'tir1'
    
  # central wavelength
  switch = {
      'AST':11.3,
      'L4':11.45,
      'L5':11.45,
      'L7':11.45,
      'L8':10.8,
      }
    
  tir_lake = tir['lake_rad'][tir_11micron]
  tir_bkgd = tir['bkgd_rad'][tir_11micron]
  central_wavelength = switch[satellite]
  
  return (tir_lake, tir_bkgd, central_wavelength)


def thermal_atmcorr(tir,satellite):
          
  tir_lake, tir_bkgd, central_wavelength = TIR_11micron(tir,satellite)
  BT_lake = planck(central_wavelength, L = tir_lake, celsius=True)
  BT_bkgd = planck(central_wavelength, L = tir_bkgd, celsius=True)
  #dTsurface = surface_deltaTemperature(tir_lake, tir_bkgd, central_wavelength)
  
  return {
  'BT_lake':BT_lake,
  'BT_bkgd':BT_bkgd,
  'dBT':BT_lake-BT_bkgd,
  #'dTsurface':dTsurface
  }