"""
Temperature difference (dT) test



"""

from physics import planck

"""
--------------
TRUE CONDITION
--------------
"""

def radianceAtSensor(T,emis,tau,Lp):
    return tau*emis*planck(wavelength,T=T) + Lp


# surface temperatures
T1 = 30
T2 = 0

# surface emissivity
e1 = 0.98 
e2 = 0.95

# atmosphere
true_tau = 1
Lp = 1

# at-sensor radiance
wavelength = 11
L1 = radianceAtSensor(T1+273.15,e1,true_tau,Lp)
L2 = radianceAtSensor(T2+273.15,e2,true_tau,Lp) 



"""
------------------
MODEL dT RETRIEVAL
------------------
"""

def dTestimate(L1,L2,model_e,model_tau):
  dL = L1-L2                       # delta radiance at sensor
  model_dL = dL/(model_e*model_tau)# estimated delta radiance at surface
  model_dT = model_dL/0.133        # linear correction from dL to dT
  return model_dT
  
# model values
model_e = 0.975       # emissivity
model_tau = true_tau  # transmissivty of atm.

# model delta temperature
model_dT = dTestimate(L1,L2,model_e,model_tau)

# delta difference
ddT = 1


"""
---------------
INSPECT RESULTS
---------------
"""
print('actual dT = ',T1-T2)
print('model_dT = ',model_dT)
print('ddT = ',model_dT-(T1-T2))

























