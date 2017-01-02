def get_predefined_wavelength(sensor):
  
  if sensor == 'ASTER':
    channels = {
    'B1':PredefinedWavelengths.ASTER_B1,
    'B2':PredefinedWavelengths.ASTER_B2,
    'B3B':PredefinedWavelengths.ASTER_B3B,
    'B3N':PredefinedWavelengths.ASTER_B3N,
    'B4':PredefinedWavelengths.ASTER_B4,
    'B5':PredefinedWavelengths.ASTER_B5,
    'B6':PredefinedWavelengths.ASTER_B6,
    'B7':PredefinedWavelengths.ASTER_B7,
    'B8':PredefinedWavelengths.ASTER_B8,
    'B9':PredefinedWavelengths.ASTER_B9
    }
  
  if sensor == 'LANDSAT_TM':
    channels = {
    'B1':PredefinedWavelengths.LANDSAT_TM_B1,
    'B2':PredefinedWavelengths.LANDSAT_TM_B2,
    'B3':PredefinedWavelengths.LANDSAT_TM_B3,
    'B4':PredefinedWavelengths.LANDSAT_TM_B4,
    'B5':PredefinedWavelengths.LANDSAT_TM_B5,
    'B7':PredefinedWavelengths.LANDSAT_TM_B7,
    }
    
  if sensor == 'LANDSAT_ETM':
    channels = {
    'B1':PredefinedWavelengths.LANDSAT_ETM_B1,
    'B2':PredefinedWavelengths.LANDSAT_ETM_B2,
    'B3':PredefinedWavelengths.LANDSAT_ETM_B3,
    'B4':PredefinedWavelengths.LANDSAT_ETM_B4,
    'B5':PredefinedWavelengths.LANDSAT_ETM_B5,
    'B7':PredefinedWavelengths.LANDSAT_ETM_B7,
    }
    
  if sensor == 'LANDSAT_OLI':
    channels = {
    'B1':PredefinedWavelengths.LANDSAT_OLI_B1,
    'B2':PredefinedWavelengths.LANDSAT_OLI_B2,
    'B3':PredefinedWavelengths.LANDSAT_OLI_B3,
    'B4':PredefinedWavelengths.LANDSAT_OLI_B4,
    'B5':PredefinedWavelengths.LANDSAT_OLI_B5,
    'B6':PredefinedWavelengths.LANDSAT_OLI_B6,
    'B7':PredefinedWavelengths.LANDSAT_OLI_B7,
    'B8':PredefinedWavelengths.LANDSAT_OLI_B8,
    'B9':PredefinedWavelengths.LANDSAT_OLI_B9,
    'PAN':PredefinedWavelengths.LANDSAT_OLI_PAN
    }
  
  # return a Py6S 'Wavelength'
  return channels
  
sensor = 'LANDSAT_TM'
print(sensor)
wavebands = get_predefined_wavelength(sensor)
channels = sorted(wavebands.keys())

for channel in channels:
  print("'{0}' : ({1[1]}, {1[2]}),".format(channel,wavebands[channel]))







