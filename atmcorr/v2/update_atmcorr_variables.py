"""
Runs 6S emulator and updates atmospheric variables

"""

import sys
import os, glob, pickle
import pandas as pd
import numpy as np
import math
import datetime

def load_iluts(aerosol):

  def load_ilut(sensor_name, aerosol):
    """
    Loads interpolated look up table (required for 6S emulation)
    """

    iLUT = {}
    band_names = ['blue','green','red','nir','swir1','swir2']

    base_path = '/home/sam/git/atmcorr_py6s/iLUTs/'
    full_path = os.path.join(base_path,sensor_name+'_'+aerosol,'viewz_0/')
    filepaths = sorted(glob.glob(full_path+'*.ilut'))

    for i, filepath in enumerate(filepaths):
      iLUT[band_names[i]] = pickle.load(open(filepath,'rb'))

    return iLUT
  
  return {
  'TM':load_ilut('LANDSAT_TM',aerosol),
  'ETM':load_ilut('LANDSAT_ETM',aerosol),
  'OLI':load_ilut('LANDSAT_OLI',aerosol)  
  }

def iLUT_select(iLUTs,p):
  """
  Selects iLUT for given satellite (i.e. L4 and L5 are both TM)
  """

  satID_to_sensor = {
  'LT4':'TM',
  'LT5':'TM',
  'LE7':'ETM',
  'LC8':'OLI'
  }

  return iLUTs[satID_to_sensor[p['satID']]]

def elliptical_orbit_correction(p):
  """
  Correction coefficient from perihelion to day of year
  """

  # day of year
  date = datetime.datetime.strptime(p['datetime'],'%Y-%m-%dT%H:%M:%S')
  doy = date.timetuple().tm_yday

  # constants
  a = 0.03275
  b = 18.992
  c = 0.968047

  return a*np.cos(doy/(b*math.pi)) + c

def emulate_6S(iLUT,p,km):
  """
  Emulates 6S (i.e. generate single waveband correction coefficients)
  """
  # perihelion
  Edir, Edif, tau2, Lp = iLUT(p['solar_z'],p['H2O'],p['O3'],p['AOT'],km)

  # corrected for Earth's orbit
  orbit_correction = elliptical_orbit_correction(p)
  Edir = Edir * orbit_correction
  Edif = Edif * orbit_correction
  Lp   = Lp   * orbit_correction

  return (Edir,Edif,tau2,Lp)

def atmospheric_correction_coefficients(iLUTs, atmvars, km):
  
  result = []

  for i in range(len(atmvars.index)):

    print('{} of {}'.format(i+1,len(atmvars.index)))

    # parameters (atmospheric variables in row)
    p = atmvars.iloc()[i]

    # select iLUT
    iLUT = iLUT_select(iLUTs,p)

    # emulate 6S outputs
    blue  =  emulate_6S(iLUT['blue'],p,km)
    green =  emulate_6S(iLUT['green'],p,km)
    red   =  emulate_6S(iLUT['red'],p,km)
    nir   =  emulate_6S(iLUT['nir'],p,km)
    swir1 =  emulate_6S(iLUT['swir1'],p,km)
    swir2 =  emulate_6S(iLUT['swir2'],p,km)

    # append as single list
    result.append(list(blue)+list(green)+list(red)+list(nir)+list(swir1)+list(swir2))

  return result

def updated_dateframe(atmvars,atmcorr):
  
  df = atmvars

  df['blue_Edir'] = [x[0] for x in atmcorr]
  df['blue_Edif'] = [x[1] for x in atmcorr]
  df['blue_tau2'] = [x[2] for x in atmcorr]
  df['blue_Lp']   = [x[3] for x in atmcorr]

  df['green_Edir'] = [x[4] for x in atmcorr]
  df['green_Edif'] = [x[5] for x in atmcorr]
  df['green_tau2'] = [x[6] for x in atmcorr]
  df['green_Lp']   = [x[7] for x in atmcorr]

  df['red_Edir'] = [x[8] for x in atmcorr]
  df['red_Edif'] = [x[9] for x in atmcorr]
  df['red_tau2'] = [x[10] for x in atmcorr]
  df['red_Lp']   = [x[11] for x in atmcorr]

  df['nir_Edir'] = [x[12] for x in atmcorr]
  df['nir_Edif'] = [x[13] for x in atmcorr]
  df['nir_tau2'] = [x[14] for x in atmcorr]
  df['nir_Lp']   = [x[15] for x in atmcorr]

  df['swir1_Edir'] = [x[16] for x in atmcorr]
  df['swir1_Edif'] = [x[17] for x in atmcorr]
  df['swir1_tau2'] = [x[18] for x in atmcorr]
  df['swir1_Lp']   = [x[19] for x in atmcorr]

  df['swir2_Edir'] = [x[20] for x in atmcorr]
  df['swir2_Edif'] = [x[21] for x in atmcorr]
  df['swir2_tau2'] = [x[22] for x in atmcorr]
  df['swir2_Lp']   = [x[23] for x in atmcorr]

  # create fileIDs (i.e. will strip system:index to handle merged image collections)
  df['fileID'] = [x.split('_')[-1] for x in df['system:index']]

  return df


def main():

  args = sys.argv[1:]
  if not args:
    print('usage: $ python3 update_atmcorr_variables.py {target} {aerosol_profile} \n'
    'must specify at least the target name')
    return

  # target name (i.e. should be same as in export_atmcorr_variables.py)
  target = args.pop(0)

  # aerosol profile
  aerosol = 'CO'
  if args:
    if args[0] in ['CO','MA','BB','UR','DE']:
      aerosol = args[0]
    else:
      print("aerosol profile not recognized: '{}' \n"
      "will use default profile: 'CO' (i.e. continental) \n"
      "other options include: \n'MA' = maritime \n'UR' = urban\n"
      "'DE' = desert \n'BB' = biomass burning \n"
      " warning! may need to build interpolated LUTs if they don't exist already!"\
      .format(args[0]))

  # load interpolated look up tables
  iLUTs = load_iluts(aerosol)

  # atmospheric variables
  atmvars = pd.read_csv('/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/Kawah_Ijen/atmcorr/'
  'atmospheric_variables_{0}.csv'.format(target))

  # target altitude
  alts = pd.read_csv('/home/sam/git/crater_lakes/atmcorr/v2/altitudes_full.csv')
  km = alts.altitude[alts.name[alts.name.str.contains(target)].index[0]] / 1000

  # atmospheric correction (i.e. emulate 6S radiative transfer code)
  atmcorr = atmospheric_correction_coefficients(iLUTs, atmvars, km)

  # updated dateframe
  df = updated_dateframe(atmvars,atmcorr)
  
  # export to csv
  df.to_csv('/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/Kawah_Ijen/atmcorr'
  '/atmospheric_variables_{0}_{1}.csv'.format(target,aerosol),\
  columns = ['fileID','datetime','H2O','O3','AOT','solar_z',\
  'blue_Edir','blue_Edif','blue_tau2','blue_Lp',\
  'green_Edir','green_Edif','green_tau2','green_Lp',\
  'red_Edir','red_Edif','red_tau2','red_Lp',\
  'nir_Edir','nir_Edif','nir_tau2','nir_Lp',\
  'swir1_Edir','swir1_Edif','swir1_tau2','swir1_Lp',\
  'swir2_Edir','swir2_Edif','swir2_tau2','swir2_Lp',\
  ],\
  index=False)

if __name__ == '__main__':
  main()

