import pandas as pd
import datetime
from Py6S import *
from satellites import spectralResponseFunctions


# read inputs from csv
atms = pd.read_csv('/home/sam/git/crater_lakes/atmcorr/atmospheric_variables.csv')
alts = pd.read_csv('/home/sam/git/crater_lakes/atmcorr/altitudes_full.csv')
size = len(atms.index)

# target altitude
target = 'Kelimutu'
km = alts.altitude[alts.name[alts.name.str.contains(target)].index[0]] / 1000

# new outputs
Edirs = []
Edifs = []
Lps = []
tau2s = []

for i in range(size):

	print('{} of {}'.format(i+1,size))

	# data row
	d = atms.iloc()[i]

	date = datetime.datetime.strptime(d['datetime'],'%Y-%m-%dT%H:%M:%S')

	# 6S object
	s = SixS()

	# Atmospheric constituents
	s.atmos_profile = AtmosProfile.UserWaterAndOzone(d.H2O,d.O3)
	s.aero_profile = AeroProfile.Continental
	s.aot550 = d.AOT

	# Earth-Sun-satellite geometry
	s.geometry = Geometry.User()
	s.geometry.view_z = 0           # always NADIR (I think..)
	s.geometry.solar_z = d.solar_z  # solar zenith angle
	s.geometry.month = date.month   # month and day used for Earth-Sun distance
	s.geometry.day = date.day       # month and day used for Earth-Sun distance
	s.altitudes.set_sensor_satellite_level()
	s.altitudes.set_target_custom_altitude(km)

	# run 6S for this waveband
	s.wavelength = spectralResponseFunctions('LANDSAT_4','B1')
	s.run()

	# extract 6S outputs
	Edir = s.outputs.direct_solar_irradiance             #direct solar irradiance
	Edif = s.outputs.diffuse_solar_irradiance            #diffuse solar irradiance
	Lp   = s.outputs.atmospheric_intrinsic_radiance      #path radiance
	absorb  = s.outputs.trans['global_gas'].upward       #absorption transmissivity
	scatter = s.outputs.trans['total_scattering'].upward #scattering transmissivity
	tau2 = absorb*scatter                                #total transmissivity

	Edirs.append(Edir)
	Edifs.append(Edif)
	Lps.append(Lp)
	tau2s.append(tau2)

# add to dataframe
atms['Edir'] = Edirs
atms['Edif'] = Edifs
atms['Lp']   = Lps
atms['tau2'] = tau2s

# create fileIDs (i.e. from merged system:index)
atms['fileID'] = [x.split('_')[-1] for x in atms['system:index']]

# export to csv
atms.to_csv('/home/sam/git/crater_lakes/atmcorr/atmospheric_variables_6S.csv',\
	columns = ['fileID','datetime','H2O','O3','AOT','solar_z','Edir','Edif','Lp','tau2'],
	index=False)