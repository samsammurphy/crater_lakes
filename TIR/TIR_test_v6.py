#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Temperature difference (dT) test

1) estimate surface temperature
2) average of 1st derivative of plank function (i.e. at T1 and T2) = m
3) use m to solve for dT

"""

from physics import planck
import numpy as np
from matplotlib import pylab as plt


def radianceAtSensor(T,emis,tau,Lp):
  """
  radiance reaching the satellite sensor
  """
  return tau*emis*planck(wavelength,T=T) + Lp
  
def radianceAtSurface(Lsensor,emis,tau,Lp):
  """
  land-leaving radiance from at-sensor radiance
  """
  return (Lsensor-Lp)/(emis*tau)

def gradientAtTemperature(T):
  """
  1st derivative of planck function with respect to temperature
  """

  # wavelength in metres
  w = 11e-6
  
  # constants
  h = 6.626068e-34    #planck
  c = 2.997925e8      #speed of light
  k = 1.38066e-23     #boltzmann
  
  # condensed constances
  K1 = (2*h*c**2)/w**5 # per metres (i.e. SI units)
  K1 = K1 / 1e6        # per microns
  K2 = (h*c)/(k*w)   
  
  return ( K1*K2*np.exp(K2/(T)) ) / ( ((T)**2)*(np.exp(K2/(T))-1)**2 )  
  
def planck_gradient(L1,L2,model_e,model_tau,model_Lp):
  """
  Estimates gradient by
  1) estimating surface temperatures at L1 and L2
  2) getting gradients from temperatures
  3) return mean gradient
  """
  
  # surface radiance estimates
  B1 = radianceAtSurface(L1,model_e,model_tau,model_Lp)
  B2 = radianceAtSurface(L2,model_e,model_tau,model_Lp)
  
  # surface temperature estimates
  T1 = planck(wavelength,L=B1)
  T2 = planck(wavelength,L=B2)
  
  # gradient estimates
  m1 = gradientAtTemperature(T1)
  m2 = gradientAtTemperature(T2)
    
  # avergage gradient
  return (m1+m2)/2

"""
CONFIGURATION
"""
wavelength = 11 
tau_errors = [-0.05,0,0.05]
Lp_errors = [-0.5,0,0.5]
model_e = 1 # i.e. the assumed emissivity (looks like blackbody is best)


# atmospheres
taus = np.linspace(0.5,1,6)
Lps = np.linspace(1,5,5)

# surface emissivity
e1s = np.linspace(0.95,1,6)
e2s = np.linspace(0.95,1,6)

# temperature space
T2s = np.linspace(0,30,4)
true_dTs = np.linspace(0,30,4)

"""
RUN TEST
"""
results = []
for tau in taus:
  for tau_error in tau_errors:
    for Lp in Lps:
      for Lp_error in Lp_errors:
        for e1 in e1s:
          for e2 in e2s:
            for T2 in T2s:
              for dT_true in true_dTs:
                
                T1 = T2 + dT_true
      
                L1 = radianceAtSensor(T1+273.15,e1,tau,Lp)
                L2 = radianceAtSensor(T2+273.15,e2,tau,Lp) 
      
                # esimtated transmissivity and path radiance
                tau_est = tau + tau_error 
                Lp_est  = Lp + Lp_error
                
                # estimate gradient of planck function
                m = planck_gradient(L1,L2,model_e,tau_est,Lp_est)  
                
                # estimate dT from dL
                dL = L1-L2                     
                dL_surface_est = dL/(model_e*tau_est) # estimated delta radiance at surface
                dT_surface_est = dL_surface_est/m         
  
                
                # delta difference
                ddT = dT_surface_est - dT_true
                
                # append result
                result = {
                'dT_true':dT_true,
                'dT_surface_est':dT_surface_est,
                'ddT':ddT,
                'tau':tau,
                'Lp':Lp,
                'e2':e2,
                'T1':T1,
                'T2':T2,
                'L1':L1,
                'L2':L2,
                'tau_est':tau_est,
                }
                
                results.append(result)


dT_true = [x['dT_true'] for x in results]
dT_surface_est = [x['dT_surface_est'] for x in results]

ddTs = [x['ddT'] for x in results]# if dic['dT'] == 30]
plt.hist(ddTs,color='red',normed=True)
plt.title("B(T)' GRADIENT ESTIMATE")
plt.xlabel('difference in dT')
plt.ylabel('normalized frequency')
plt.xlim(-8,8)
plt.ylim(0,0.3)
plt.show()

#proportional difference
pdT = [a/b for a,b in zip(dT_surface_est,dT_true) if b != 0]
plt.hist(pdT,normed=True,color='red')
plt.title("B(T)' GRADIENT ESTIMATE")
plt.xlabel('relative dT')
plt.ylabel('normalized frequency')
plt.xlim(0.4,1.6)
plt.ylim(0,5)
plt.show()

