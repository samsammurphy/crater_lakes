
from physics import planck



# central wavelength
wavelength = 11

# true atmosphere
true_tau = 1
Lp = 1

# model atmosphere
model_tau = 1

def radianceAtSensor(T,emis,tau,Lp):
    return tau*emis*planck(wavelength,T=T) + Lp

T1 = 30
T2 = 20

L1 = radianceAtSensor(T1+273.15,1,true_tau,Lp)
L2 = radianceAtSensor(T2+273.15,1,true_tau,Lp) 

dL = L1-L2

model_dT = (dL/model_tau)/0.133


print('actual dT = ',T1-T2)
print('model_dT = ',model_dT)