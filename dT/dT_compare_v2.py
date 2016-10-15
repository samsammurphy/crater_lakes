"""
dT_compare.py, Author: Sam Murphy (2016-10-10)

Temperature difference (dT) comparison for 1) actual dT, 2) brightness dT
for a range of atmospheric transmissivities and water vapour columns


"""


from physics import planck
import numpy as np
from matplotlib import pylab as plt


def atmospheric_conditions():
  """
  Transmissivity (tau) and path radiance (Lp) can be used to describe the 
  atmosphere for the thermal infrared.
  
  These parameteres are strongly correlated through their dependence on water vapour.
  
  Pairs of (tau, Lp) should therefore take this into account. This is done using
  linear fits calculated graphically from Fig. 3 in French et al (2003)
  
  """

  #water vapour values
  water_vapour = np.linspace(1,5,5)# (atm-cm)
  
  # transmissivity and path radiance as a function of water vapour
  taus = 1+water_vapour*-0.1214
  Lps = water_vapour
  
  # pairs of tau and Lp
  return list(zip(taus,Lps))

def atSensorRadiance(T,w,atm):
  """
  calculate at sensor radiance given Temperature, wavelength, transmissivity
  and path radiance
  """
  ground_radiance = planck(w,T=T)   
  tau = atm[0]
  Lp = atm[1]
  return tau*ground_radiance + Lp  
  
  
# wavelength (microns)
w = 11
  
# atmospheres (tau,Lp)
atms = atmospheric_conditions()

# surface temperatures (kelvins)
Tbkgd = np.linspace(0,30,4)+273  # background
delta = np.linspace(0,20,21)        # lake temperature above background


# results lists
comparisons = []

for atm in atms:
  for Tb in Tbkgd:
    for dT in delta:
      
      # lake temperature
      Tl = Tb + dT
      
      # radiances
      Lb = atSensorRadiance(Tb,w,atm)
      Ll = atSensorRadiance(Tl,w,atm)
      
      # brightness difference
      dL = Ll-Lb
      bD = planck(w,L=dL)
      comparisons.append((dT,dL,bD))


dT = np.array([c[0] for c in comparisons])
dL = np.array([c[1] for c in comparisons])
bD = np.array([c[2] for c in comparisons])

plt.plot(dT,bD)

