"""
Temperature difference (dT) retrieval test

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
  m1 = 0.00115482*(T1-273.15) + 0.11001702
  m2 = 0.00115482*(T2-273.15) + 0.11001702
  
  # avergage gradient
  return (m1+m2)/2


def dTestimate(L1,L2,model_e,model_tau,model_Lp):
  """
  delta temperature estimate from at-sensor radiance, and model emissivity
  and model transmissivity
  """
  
  # estimate gradient of planck function
  m = planck_gradient(L1,L2,model_e,model_tau,model_Lp)  
  
  # estimate dT from dL
  dL = L1-L2                       # delta radiance at sensor
  model_dL = dL/(model_e*model_tau)# estimated delta radiance at surface
  return model_dL/m                # linear correction of dL to dT





# satellite waveband
wavelength = 11 
"""the wavelength is hardcoded for now, updates would require recalculation 
of gradient, m, using dPlanck.py
"""
  
  
# sensitivity analysis
dTaus = [-0.05,0,0.05]
dLps = [-0.5,0,0.5]
model_e = 1


# atmospheres
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
      for dLp in dLps:
        for e2 in e2s:
          for T2 in T2s:
            for dT in dTs:
              
              T1 = T2 + dT
    
              L1 = radianceAtSensor(T1+273.15,e1,tau,Lp)
              L2 = radianceAtSensor(T2+273.15,e2,tau,Lp) 
    
              # model delta temperature
              model_tau = tau+dTau  # transmissivity
              model_Lp = Lp+dLp     # path radiance
              model_dT = dTestimate(L1,L2,model_e,model_tau,model_Lp)
              
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

plt.plot(dT,model_dT,color='green')
plt.title('linear GRADIENT')
plt.xlabel('dT')
plt.ylabel('model dT')
plt.plot(dT,dT,'-r')
plt.show()


ddTs = [dic['ddT'] for dic in results]# if dic['dT'] == 30]
plt.hist(ddTs,color='green',normed=True)
plt.title('linear GRADIENT')
plt.xlabel('difference in dT')
plt.ylabel('normalized frequency')
plt.xlim(-8,8)
plt.show()

print('means ddT = ',np.mean(ddTs))















