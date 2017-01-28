"""
Linear model of planck function

Gradient is derived from average of B(T)' at two points.

"""

import numpy as np
from matplotlib import pylab as plt

def plank_1st_derivative(T):
  """
  1st derivative of plank function B(T)
  """ 
  
  return ( K1*K2*np.exp(K2/(T+273.15)) ) / ( ((T+273.15)**2)*(np.exp(K2/(T+273.15))-1)**2 )


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

# temperature, B(T)' 
plt.plot(T,plank_1st_derivative(T))
plt.title('Planck gradient at 11 microns')
plt.xlabel('Temperature (oC)')
plt.ylabel('m')
plt.show()

# gradient from B(T)' sample
T1 = 0
T2 = 60
m1 = plank_1st_derivative(T1)
m2 = plank_1st_derivative(T2)
m = np.mean([m1,m2])

print(m1,m2)

# linear fit
c = K1/(np.exp(K2/(0+273.15))-1)
linearFit = m*T+c

# temperature, B(T)
plt.plot(T,L,linewidth=3,color='gray')
plt.title('Radiance at 11 microns')
plt.xlabel('Temperature (oC)')
plt.ylabel('Radiance')

plt.plot(T, linearFit, '--r',linewidth=2)
plt.show()