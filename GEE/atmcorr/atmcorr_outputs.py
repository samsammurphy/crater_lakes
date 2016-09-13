# -*- coding: utf-8 -*-
"""

Atmospheric correction outputs

"""

import glob
import pickle
import csv
import numpy as np
import math
import datetime

def load_iLUT(ilut_path):
  """
  Loads an interpolated lookup tables for a given sensor
  """
  fnames = glob.glob(ilut_path+'*.ilut')
  fnames.sort()
  iLUT = {
  'blue' : pickle.load(open(fnames[0], "rb" )),
  'green': pickle.load(open(fnames[1], "rb" )),
  'red'  : pickle.load(open(fnames[2], "rb" )),
  'nir'  : pickle.load(open(fnames[3], "rb" )),
  'swir1': pickle.load(open(fnames[4], "rb" )),
  'swir2': pickle.load(open(fnames[5], "rb" ))
  }

  return iLUT


def read_iLUTs():
  """
  Read interpolated look-up tables for L7 and L8 (MA,0) ONLY
  """
  base_path = '/media/sam/DataDisk/GoogleDrive/atmcorr/iLUT/'
  ETMplus = load_iLUT(base_path+'LANDSAT_ETM_MA/viewz_0/')
  OLI = load_iLUT(base_path+'LANDSAT_OLI_MA/viewz_0/') 
  
  return {'ETM+':ETMplus,'OLI':OLI}


def read_inputs(target):
  """
  read atmospheric correction inputs
  
  i.e. altitude, solar_z, view_z, H2O, O3, AOT_stats
  """
  base_path = '/home/sam/Desktop/quick_push/'
  fname = target+'_atmcorr_inputs.csv'
  
  input_variables = list()
  
  with open(base_path+fname, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    
    # read altitude from header
    header = next(reader, None)[0]
    altitude = float(header.split('|')[0].split('=')[-1]) / 1000 #convert from metres to km
    
    # function to convert H2O units (Google = kg/m^2, Py6S = g/cm^2)
    def convert_H2O_units(H2O_google):
      return float(H2O_google) * 1000 / 10000 #(i.e. kg to g multiple by 1000, 1/m2 to 1/cm2 divide by 10000)
    
    # function to convert O3 units (Google = Dobson Units, Py6S = atm-cm)
    def convert_O3_units(O3_google):
      return float(O3_google) / 1000 # (i.e. Dobson units are milli-atm-cm )
    
    def AOT_stat(string):
      if string == 'null':
        return 0
      else:
        return float(string)
    
    for row in reader:
      
      fileID = row[0]
      timestamp = float(row[1])
      solar_z = float(row[2])
      view_z = float(row[3])
      H2O = convert_H2O_units(row[4])
      O3 = convert_O3_units(row[5])
      AOT_split = row[6].split("'")
      AOT_stats = {
      'count_nir':  AOT_stat(AOT_split[1]),
      'count_swir2':AOT_stat(AOT_split[3]),
      'count_ndwi': AOT_stat(AOT_split[5]),
      'mean_nir':   AOT_stat(AOT_split[7]),
      'mean_swir2': AOT_stat(AOT_split[9]),
      'mean_ndwi'  :AOT_stat(AOT_split[11])    
      }
      
      input_variables.append({'fileID':fileID,'timestamp':timestamp,
      'solar_z':solar_z,'view_z':view_z,'H2O':H2O,'O3':O3,'AOT_stats':AOT_stats})

  return altitude, input_variables
    
    
def surface_reflectance(L, iLUTx, v, model_AOT, alt):
  
  # harmonic function for elliptical orbit correction
  def simple_harmonic(doy, a,b,c): return a*np.cos(doy/(b*math.pi)) + c
    
  # day-of-year (i.e. used in harmonic function)
  def doy_from_timestamp(timestamp):
    d = datetime.datetime.fromtimestamp(timestamp)
    doy = (d - datetime.datetime(d.year, 1, 1) + datetime.timedelta(1)).days
    return doy 
  
  # correction coefficients at perihelion
  Edir, Edif, tau2, Lp = iLUTx(v['solar_z'],v['H2O'],v['O3'], model_AOT, alt)
  
  # elliptical orbit correction
  doy = doy_from_timestamp(v['timestamp'])
  Edir = Edir * simple_harmonic(doy, 0.0327505,   18.99181408 ,  0.96804793)
  Edif = Edif * simple_harmonic(doy, 0.03275025,  18.99238934 ,  0.96805088)
  Lp   = Lp   * simple_harmonic(doy, 0.0327459 ,  18.99219987 ,  0.96804217)
  
  #surface reflectance
  ref = (math.pi*(L-Lp))/(tau2*(Edir+Edif))
  
  return ref

# aerosol optical thickness (water pixel ratio method of Kaufmann et al. 2008)
def get_AOT(v, altitude, iLUT):
  
  # model AOTs values (0.001 to 3 in 5% increments)
  model_AOTs = [0.001]
  while np.max(model_AOTs)*1.05 < 3:
    model_AOTs.append(np.max(model_AOTs)*1.05)

  # water stats for AOT retrieval
  nir = v['AOT_stats']['mean_nir']
  swir2 = v['AOT_stats']['mean_swir2']
  
  # model surface reflectance ratios
  ratios = list()
  for model_AOT in model_AOTs:
    nir_SR   = surface_reflectance(nir, iLUT['nir'], v, model_AOT, altitude)
    swir2_SR = surface_reflectance(swir2, iLUT['swir2'], v, model_AOT, altitude)
    ratios.append(swir2_SR/nir_SR)  
    
  # find ratio closest to 0.81
  diff = abs(np.array(ratios)-0.81)
  match = np.where(diff == np.min(diff))[0][0]
  
  return model_AOTs[match]

# sensor name from file ID
def sensor_name_from_fileID(fileID):
  
  # satelliteID from fileID
  ID = fileID[0:3]
  
  # sensor from satelliteID  
  if ID == 'LT4' or ID == 'LT5': sensor = 'TM'
  if ID == 'LE7': sensor = 'ETM+'
  if ID == 'LC8': sensor = 'OLI'
  
  return sensor
  
# atmospheric correction using iLUT simulation of Py6S
def atmcorr(altitude, input_variables, iLUTs):
    
  outputs = list()
  for v in input_variables:  
    stats = v['AOT_stats'] # use stats to determine if lake water pixels found
    if stats['count_nir'] > 0:
      #iLUT for this sensor
      iLUT = iLUTs[sensor_name_from_fileID(v['fileID'])]
      #estimate aerosol optical thickness
      AOT = get_AOT(v, altitude, iLUT)
      print(v['fileID']+' AOT = ',AOT)      
      
      #atmospheric correction coefficients
      coeffs = {
      'fileID':v['fileID'],'AOT':AOT,
      'blue':iLUT['blue'](v['solar_z'],v['H2O'],v['O3'],AOT,altitude),
      'green':iLUT['green'](v['solar_z'],v['H2O'],v['O3'],AOT,altitude),
      'red':iLUT['red'](v['solar_z'],v['H2O'],v['O3'],AOT,altitude),
      'nir':iLUT['nir'](v['solar_z'],v['H2O'],v['O3'],AOT,altitude),
      'swir1':iLUT['swir1'](v['solar_z'],v['H2O'],v['O3'],AOT,altitude),
      'swir2':iLUT['swir2'](v['solar_z'],v['H2O'],v['O3'],AOT,altitude)
      }
  
      #append to output list
      outputs.append(coeffs)

  else:
    print('no lake water pixels found in: '+v['fileID'])
    
  return outputs
  

# write atmcorr outputs to file
def write_outputs(outputs):
  
  with open('/home/sam/Desktop/atmcorr_outputs.csv', 'w') as outfile:
    writer = csv.writer(outfile, delimiter=',')
    writer.writerow(['fileID AOT '
                     'b_Edir b_Edif b_tau2 b_Lp '
                     'g_Edir g_Edif g_tau2 g_Lp '
                     'r_Edir r_Edif r_tau2 r_Lp '
                     'n_Edir n_Edif n_tau2 n_Lp '
                     's1_Edir s1_Edif s1_tau2 s1_Lp '
                     's2_Edir s2_Edif s2_tau2 s2_Lp'])
                             
    def output_to_string(arr): return '{} {} {} {}'.format(arr[0],arr[1],arr[2],arr[3])
        
    for out in outputs:    
      ID = out['fileID']  
      AOT = out['AOT']
      b = output_to_string(out['blue'])  
      g = output_to_string(out['green']) 
      r = output_to_string(out['red']) 
      n = output_to_string(out['nir']) 
      s1 = output_to_string(out['swir1']) 
      s2 = output_to_string(out['swir2']) 
      
      writer.writerow(['{} {} {} {} {} {} {}'.format(ID,AOT,b,g,r,n,s1,s2)])
  
  return 1

def main():

  iLUTs = read_iLUTs()    
  
  target = 'Aoba'
  altitude, input_variables = read_inputs(target)
  outputs = atmcorr(altitude, input_variables, iLUTs)
  write_outputs(outputs)

if __name__ == '__main__':
  main()