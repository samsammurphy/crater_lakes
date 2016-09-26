#PYTHON

import numpy as np
from surface_reflectance import surface_reflectance as SR

## aerosol optical thickness (water pixel ratio method; Kaufmann et al. 2008)
def get_AOT(lake_mean_rad, iLUTs, scene_info):

  # model AOTs values (from 0.001 to 3 in 5% increments)
  model_AOTs = [0.001]
  while np.max(model_AOTs)*1.05 < 3:
    model_AOTs.append(np.max(model_AOTs)*1.05)
    
  # ratios of potetnial surface reflectance
  ratios = list()
  for model_AOT in model_AOTs:
    
    scene_info['AOT'] = model_AOT
    
    SR_nir = SR(lake_mean_rad['nir'], iLUTs['nir'], scene_info)
    SR_swir2 = SR(lake_mean_rad['swir2'], iLUTs['swir2'], scene_info)
    
    ratio = SR_swir2 / SR_nir
    ratios.append(ratio)
    
    
  # return AOT where ratio closest to 0.81
  diff = abs(np.array(ratios)-0.81)
  match = np.where(diff == np.min(diff))[0][0]
    
  return model_AOTs[match]