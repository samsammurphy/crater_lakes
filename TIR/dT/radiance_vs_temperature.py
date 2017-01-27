"""
Plot radiance as a function of temperature

"""

import numpy as np
from physics import planck
from matplotlib import pylab as plt


# waveband (microns)
wavelength = 11

# temperature (celsius)
temps = np.linspace(0,60,61)+273

# radiance
L = np.array([planck(wavelength,T=T) for T in temps])

# radiance vs temperature plot
plt.plot(temps-273,L,linewidth=3,color='gray')
plt.title('Radiance at 11 microns')
plt.xlabel('Temperature (oC)')
plt.ylabel('Radiance')
plt.ylim(4,16)

# linear fit
fit = np.polyfit(temps-273,L,1)
fit_fn = np.poly1d(fit)# fit_fn is a function which takes in x and returns an estimate for y
plt.plot(temps-273, fit_fn(temps-273), '--r',linewidth=2)
plt.show()
print('gradient = ',fit)