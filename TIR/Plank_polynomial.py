"""
Polynomial fit to Planck function

"""

import numpy as np
from matplotlib import pylab as plt

def polyfit(x,y):
  """
  linear fit of x,y (returns linearized y)
  """
  fit = np.polyfit(x,y,2)
  fit_fn = np.poly1d(fit)
  yy = fit_fn(x) 
  
  return yy

# constants
h = 6.626068e-34    # planck
c = 2.997925e8      # speed of light
k = 1.38066e-23     # boltzmann
w = 11 / 1e6        # wavelength

# condensed constants
K1 = (2*h*c**2)/w**5 # per metres
K1 = K1 / 1e6         # per micron
K2 = (h*c)/(k*w) 

# temperature space
T = np.linspace(0,60,61)

# blackbody radiance (plank function)
L = K1/(np.exp(K2/(T+273.15))-1)

# temperature, blackbody radiance
plt.plot(T,L,linewidth=3,color='gray')
plt.title('Radiance at 11 microns')
plt.xlabel('Temperature (oC)')
plt.ylabel('Radiance')

# linear temperature, blackbody radiance
LL = polyfit(T,L)
plt.plot(T, LL, '--r',linewidth=2)
plt.show()

