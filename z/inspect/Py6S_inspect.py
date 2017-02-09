from Py6S import *

def get_predefined_wavelength(sensor,channel):
  
  if sensor == 'TM':
    switch = {
    'B1':PredefinedWavelengths.LANDSAT_TM_B1,
    'B2':PredefinedWavelengths.LANDSAT_TM_B2,
    'B3':PredefinedWavelengths.LANDSAT_TM_B3,
    'B4':PredefinedWavelengths.LANDSAT_TM_B4,
    'B5':PredefinedWavelengths.LANDSAT_TM_B5,
    'B7':PredefinedWavelengths.LANDSAT_TM_B7,
    }
  
  if sensor == 'ETM':
    switch = {
    'B1':PredefinedWavelengths.LANDSAT_ETM_B1,
    'B2':PredefinedWavelengths.LANDSAT_ETM_B2,
    'B3':PredefinedWavelengths.LANDSAT_ETM_B3,
    'B4':PredefinedWavelengths.LANDSAT_ETM_B4,
    'B5':PredefinedWavelengths.LANDSAT_ETM_B5,
    'B7':PredefinedWavelengths.LANDSAT_ETM_B7,
    }
  
  return Wavelength(switch[channel])

def run_6S(sensor,channel,solar_z,H2O,O3,AOT,alt):
  s = SixS()
  s.altitudes.set_sensor_satellite_level()
  s.aero_profile = AeroProfile.Maritime
  s.geometry = Geometry.User()
  s.geometry.view_z = 0
  s.geometry.month = 1
  s.geometry.day = 4
  s.geometry.solar_z = solar_z
  s.atmos_profile = AtmosProfile.UserWaterAndOzone(H2O,O3)
  s.aot550 = AOT
  s.altitudes.set_target_custom_altitude(alt)
  s.wavelength = get_predefined_wavelength(sensor,channel)
  
  # run 6S
  s.run()
  # extract transmissivity
  absorb  = s.outputs.trans['global_gas'].upward       #absorption transmissivity
  scatter = s.outputs.trans['total_scattering'].upward #scattering transmissivity
  #define output variables
  Edir = s.outputs.direct_solar_irradiance             #direct solar irradiance
  Edif = s.outputs.diffuse_solar_irradiance            #diffuse solar irradiance
  Lp   = s.outputs.atmospheric_intrinsic_radiance      #path radiance
  tau2 = absorb*scatter                                #transmissivity (from surface to sensor)
  #append to outputs list
  return (Edir,Edif,tau2,Lp)
  
  
sensor = 'TM'
channel = 'B1'
solar_z = 0
H2O = 0
O3 = 0
AOT = 0
alt = 0
print('TM',run_6S('TM',channel,solar_z,H2O,O3,AOT,alt))
print('ETM',run_6S('ETM',channel,solar_z,H2O,O3,AOT,alt))
    




