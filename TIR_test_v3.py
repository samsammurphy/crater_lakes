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
  model_dT = model_dL/m            # linear correction from dL to dT
  return model_dT


# CONFIGURATION VARIABLES
m = 0.14435441 # gradient for linear correction (previously m = 0.133)
dTaus = [-0.05,0,0.05]       # error in transmissivity estimate
model_e = 1  # 0.975 emissivity



# satellite waveband
wavelength = 11
  
# atmosphere
taus = np.linspace(0.5,1,6)
Lps = np.linspace(1,5,5)

# surface emissivity
e1 = 0.98 
e2s = np.linspace(0.95,0.99,5)

# temperature space
T2s = np.linspace(0,30,7)
dTs = np.linspace(0,30,7)

# run test
results = []
for tau in taus:
  for dTau in dTaus:
    for Lp in Lps:
      for e2 in e2s:
        for T2 in T2s:
          for dT in dTs:
            
            T1 = T2 + dT
  
            L1 = radianceAtSensor(T1+273.15,e1,tau,Lp)
            L2 = radianceAtSensor(T2+273.15,e2,tau,Lp) 
  
            # model delta temperature
            model_tau = tau+dTau  # transmissivity
            model_dT = dTestimate(L1,L2,model_e,model_tau)
            
            # delta difference
            ddT = model_dT - dT
            
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
            'ddT':ddT
            }
            
            results.append(result)


dT = [dic['dT'] for dic in results]
model_dT = [dic['model_dT'] for dic in results]

plt.plot(dT,model_dT)
plt.title('Linear RADIANCE')
plt.xlabel('dT')
plt.ylabel('model dT')
plt.plot(dT,dT,'-r')
plt.show()


ddTs = [dic['ddT'] for dic in results]# if dic['dT'] == 30]
plt.hist(ddTs,normed=True)
plt.title('Linear RADIANCE')
plt.xlabel('difference in dT')
plt.ylabel('normalized frequency')
plt.xlim(-8,8)
plt.ylim(0,0.3)
plt.show()

print('means ddT = ',np.mean(ddTs))














