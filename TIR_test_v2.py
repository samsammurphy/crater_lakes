"""
Temperature difference (dT) retrieval test

"""

from physics import planck
import numpy as np
from matplotlib import pylab as plt


def radianceAtSensor(T,emis,tau,Lp):
    return tau*emis*planck(wavelength,T=T) + Lp

def dTestimate(L1,L2,model_e,model_tau):
  dL = L1-L2 # delta radiance at sensor
  model_dL = dL/(model_e*model_tau)# estimated delta radiance at surface
  model_dT = model_dL/0.133        # linear correction from dL to dT
  return model_dT
  
  
# satellite waveband
wavelength = 11
  
# atmosphere
true_taus = np.linspace(0.5,1,6)
Lps = np.linspace(1,5,5)

# surface emissivity
e1 = 0.98 
e2s = np.linspace(0.95,1,6)

# temperature space
T2s = np.linspace(0,30,31)
dTs = np.linspace(0,30,31)

# run test
results = []
for tau in true_taus:
  for Lp in Lps:
    for e2 in e2s:
      for T2 in T2s:
        for dT in dTs:
          
          T1 = T2 + dT

          L1 = radianceAtSensor(T1+273.15,e1,tau,Lp)
          L2 = radianceAtSensor(T2+273.15,e2,tau,Lp) 

          # model delta temperature
          model_e = 0.975  # emissivity
          model_tau = tau  # transmissivity
          model_dT = dTestimate(L1,L2,model_e,model_tau)
          
          # delta difference
          ddT = model_dT - dT
          pdT = dT / model_dT
          
          # append result
          result = {
          'tau':tau,
          'Lp':Lp,
          'e2':e2,
          'T2':T2,
          'dT':dT,
          'T1':T1,
          'L1':L1,
          'L2':L2,
          'model_tau':model_tau,
          'model_dT':model_dT,
          'ddT':ddT,
          'pdT':pdT
          }
          
          results.append(result)


ddTs = [dic['ddT'] for dic in results]# if dic['dT'] == 30]
plt.hist(ddTs)
plt.title('Estimating dT')
plt.xlabel('difference in dT')
plt.ylabel('frequency')
plt.xlim(-6,12)
















