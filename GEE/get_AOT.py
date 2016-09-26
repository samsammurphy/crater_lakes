import numpy as np
from surface_reflectance import surface_reflectance

# aerosol optical thickness (water pixel ratio method; Kaufmann et al. 2008)
def get_AOT(data, iLUTs):

  #lake radiance
  lake_rad = data['lake_rad']
  
  # model AOTs values (from 0.001 to 3 in 5% increments)
  model_AOTs = [0.001]
  while np.max(model_AOTs)*1.05 < 3:
    model_AOTs.append(np.max(model_AOTs)*1.05) 
  
  # ratios of potential surface reflectances
  ratios = []
  for AOT in model_AOTs:
    
    data['AOT'] = AOT
    
    #near infrared (0.8 microns)
    SR_nir = surface_reflectance(lake_rad['nir'], iLUTs['nir'],data)
    
    #short-wave infrared (2.2 microns)
    SR_swir2 = surface_reflectance(lake_rad['swir2'], iLUTs['swir2'],data)
    
    ratio = SR_swir2 / SR_nir
    ratios.append(ratio)
    
    
  # return AOT where ratio closest to 0.81
  diff = abs(np.array(ratios)-0.81)
  match = np.where(diff == np.min(diff))[0][0]
    
  return model_AOTs[match]