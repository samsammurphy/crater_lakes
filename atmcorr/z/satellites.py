"""
Helper function to more conveniently store spectral response functions for satellites
"""

from Py6S import *

def spectralResponseFunctions(satellite_name,band_name):

	# Thematic Mapper
	LANDSAT_TM = {\
	'B1':PredefinedWavelengths.LANDSAT_TM_B1,\
	'B2':PredefinedWavelengths.LANDSAT_TM_B2,\
	'B3':PredefinedWavelengths.LANDSAT_TM_B3,\
	'B4':PredefinedWavelengths.LANDSAT_TM_B4,\
	'B5':PredefinedWavelengths.LANDSAT_TM_B5,\
	'B7':PredefinedWavelengths.LANDSAT_TM_B7 \
	}

	# Enhanced Thematic Mapper Plus
	LANDSAT_ETMplus = {\
	'B1':PredefinedWavelengths.LANDSAT_ETM_B1,\
	'B2':PredefinedWavelengths.LANDSAT_ETM_B2,\
	'B3':PredefinedWavelengths.LANDSAT_ETM_B3,\
	'B4':PredefinedWavelengths.LANDSAT_ETM_B4,\
	'B5':PredefinedWavelengths.LANDSAT_ETM_B5,\
	'B7':PredefinedWavelengths.LANDSAT_ETM_B7 \
	}

	# Optical Land Imager
	LANDSAT_OLI = {\
	'B2':PredefinedWavelengths.LANDSAT_OLI_B2,\
	'B3':PredefinedWavelengths.LANDSAT_OLI_B3,\
	'B4':PredefinedWavelengths.LANDSAT_OLI_B4,\
	'B5':PredefinedWavelengths.LANDSAT_OLI_B5,\
	'B6':PredefinedWavelengths.LANDSAT_OLI_B6,\
	'B7':PredefinedWavelengths.LANDSAT_OLI_B7,\
	'PAN':PredefinedWavelengths.LANDSAT_OLI_PAN\
	}

	satellites = {\
	'LANDSAT_4':LANDSAT_TM,\
	'LANDSAT_5':LANDSAT_TM,\
	'LANDSAT_7':LANDSAT_ETMplus,\
	'LANDSAT_8':LANDSAT_OLI\
	}

	return Wavelength(satellites[satellite_name][band_name])