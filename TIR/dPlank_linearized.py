"""
Linear model of 1st derivative of planck function, B(T)

1) Plot B(T) with linear fit
2) Plot B(T)' with linear fit
3) Plot B(T) with gradient from linear fit in (2)

"""

import numpy as np
from matplotlib import pylab as plt

def linearfit(x,y):
  """
  linear fit of x,y (returns linearized y)
  """
  fit = np.polyfit(x,y,1)
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

"""
Plot 1: B(T) with linear fit
"""
# temperature, blackbody radiance
plt.plot(T,L,linewidth=3,color='gray')
plt.title('Radiance at 11 microns')
plt.xlabel('Temperature (oC)')
plt.ylabel('Radiance')

# linear temperature, blackbody radiance
LL = linearfit(T,L)
plt.plot(T, LL, '--r',linewidth=2)
plt.show()


"""
Plot 2: B(T)', 1st derivative of plank (a.k.a. dL/dT) with linear fit
"""

# 1st derivative of planck function
Bprime = ( K1*K2*np.exp(K2/(T+273.15)) ) / ( ((T+273.15)**2)*(np.exp(K2/(T+273.15))-1)**2 )

# temperature, B(T)' 
plt.plot(T,Bprime)
plt.title('Planck gradient at 11 microns')
plt.xlabel('Temperature (oC)')
plt.ylabel('m')

# linear gradient, temperature
M = linearfit(T,Bprime)
plt.plot(T, M, '--r',linewidth=2)
plt.show()


"""
Plot 3: B(T) with M gradient (i.e. linear fit of B(T)' from previous)
"""

# temperature, blackbody radiance
plt.plot(T,L,linewidth=3,color='gray')
plt.title('Radiance at 11 microns')
plt.xlabel('Temperature (oC)')
plt.ylabel('Radiance')

# M model fit
print()

# y intercept
c = L[np.where(T==0)[0]]
LL = Bprime*(T) + c
plt.plot(T, LL, '--r',linewidth=2)
plt.show()

## linear fit of gradient
#fit = np.polyfit(T,m,1)
#fit_fn = np.poly1d(fit)
#plt.plot(T, fit_fn(T), '--r',linewidth=2)
#plt.show()
#
## model gradient from temperature
#print('linear model of 2nd derivative of Planck function:\n\n'
#'m = {}*(T) + {}'.format(fit[0],fit[1]))
