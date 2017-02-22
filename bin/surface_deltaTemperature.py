#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Motivation

Surface temperature using a single TIR waveband is not (usually) reliable when 
using historic data sets because atmospheric profiles are (typically) not 
sufficiently well constrained.

Split-window is the de facto standard

However,

1) Landsat 7 (most of the data) has only one waveband
2) A consistent metric is important when using multi-sensor data sets

Previous Work has highlighted that both transmissivity and path radiance are 
linearly correlated to water vapour concentration in the TIR wavelengths, 
however, the scatter from a linear fit can result in surface temperature errors
of around 7oC (French et al. 2003).

Path radiance is the single largest source of error between surface leaving
radiance and at-sensor radiance. We can mitigate the effect of path radiance
by subtracting the radiance between the lake and the surrounding background area

dL = ετ(B1) - ετ(B2)

If both targets are close to blackbodies then

dL/τ = dB

We have therefore reduced the problem to a single unknown (i.e. τ). If we can
estimate τ to +- 0.05 using water vapour profiles (e.g. from NCEP reanalysis) 
then the following method for dT retrieval is good to
within 2oC, 90% of the time.


delta Temperature (dT)
--------------------------------

The planck function is approximately linear in the TIR in B vs T space,
where B = blackbody radiance and T = temperature
 
A simple straight line fit to the planck function could be used to estimate
the temperature difference (dT) between two blackbody surfaces
 
dT = dB / m 
 
where m is the gradient dB/dT

Lets start here: 
  
Using a simple straight line will get to within 5oC, 90 % of the time. 


TODO NEW METHOD
---------------

You could estimate the temperature of the lake and the background to localize
yourself (more or less) in B-T space. You could then calculate the gradient 
between these two temperature estimates. If they are less than 5oC appart then
you could use the gradient between +- 2.5oC from their mean.


PREVIOUS IDEA
-------------

We found
that estimating m locally provides better results. That is, to first derive
a rough estimate for the surface temperature (i.e. using water vapour derived
τ and Lp) of the target and the background, then calculate the 
derivative of the planck function at each of these temperatures, then take the
average value of these derivative as our local estimate for m.

Using this local m we can estimate dT to within 2oC, 90% of the time.

"""

from physics import planck


def waterVapour_to_transmissivity(w):
  """
  Estimate transmissivity using water vapour concentration
  
  NOTE: this is an initial ROUGH estimate, can improve.
  """
  return 1 - w/10


def planck_gradient(wavelength):
  """
  Linearize the planck function and return the gradient
  
  TODO: Use temperature estimates of the surface and find the local gradient
  """
  
  # temperature range
  T1 = 0
  T2 = 60
  
  # blackbody radiance 
  B1 = planck(wavelength,T=T1+273.15)
  B2 = planck(wavelength,T=T2+273.15)
  
  # simple gradient
  m = (B2-B1)/(T2-T1)
  
  return m

  
def surface_deltaTemperature(tir_lake, tir_bkgd, central_wavelength):
  """
  Estimate the difference in temperature between two targets in an image.
  Assumes that they are 1) blackbodies, 2) have same path radiance
  """
  
  # delta at-sensor radiance
  dL = tir_lake - tir_bkgd
  
  # estimate transmissivity from water vapour
  tau = waterVapour_to_transmissivity(water_vapour)
  
  # estimate surface delta blackbody radiance (i.e. assumed ε = 1 )
  dB = dL / tau
  
  # estimate planck gradient
  m = planck_gradient(central_wavelength)
  
  # temperature difference
  dT = dB/m
  
  return dT





  



