"""
Derivative of planck function
"""

import numpy as np
from matplotlib import pylab as plt

# constants
h = 6.626068e-34    # planck
c = 2.997925e8      # speed of light
k = 1.38066e-23     # boltzmann
w = 11 / 1e6        # wavelength

# condensed constants
a = (2*h*c**2)/w**5 # per metres
a = a / 1e6         # per micron
b = (h*c)/(k*w) 

# temperature
T = np.linspace(0,60,61)+273.15

# planck function
L = a/(np.exp(b/T)-1)

# derivative of planck function
m = ( a*b*np.exp(b/T) ) / ( (T**2)*(np.exp(b/T)-1)**2 )

# radiance vs temperature plot
plt.plot(temps-273.15,L,linewidth=3,color='gray')
plt.title('Radiance at 11 microns')
plt.xlabel('Temperature (oC)')
plt.ylabel('Radiance')
plt.show()

# gradient vs temperature plot
plt.plot(T-273.15,m)
plt.title('Planck gradient at 11 microns')
plt.xlabel('Temperature (oC)')
plt.ylabel('m')

# linear fit of gradient
fit = np.polyfit(temps-273.15,m,1)
fit_fn = np.poly1d(fit)
plt.plot(temps-273.15, fit_fn(temps-273.15), '--r',linewidth=2)
plt.show()
print('gradient = ',fit)

# model gradient from temperature
mm = 0.00115482*(T-273.15) + 0.11001702

