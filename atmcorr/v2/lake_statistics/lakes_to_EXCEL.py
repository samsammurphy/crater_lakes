import os
import glob
import json
import itertools
import colorsys
import datetime
import pandas as pd
import numpy as np

import sys
sys.path.append('/home/sam/git/crater_lakes/bin')
from baddies import naughty_list

def remove_baddies(fc, target):
  """
  Removes bad files from feature collection 
  1) from bad fileID list
  2) from not in cloud_filtered_(manually)/
  """
  
  # full fileIDs and dates (these lists will be cloud filtered in level up)
  fileIDs = [x['properties']['fileID'] for x in fc]
  dates = [datetime.datetime.utcfromtimestamp(x['properties']['timestamp']) for x in fc]
  bad_files = naughty_list(target, fileIDs, dates)
  ok = np.array([x['properties']['fileID'] not in bad_files for x in fc])
  
  return np.compress(ok, fc)

def getSR(fc, bandname):
  """
  surface reflectance time series from feature collection
  """
  return [feature['properties']['lake_SR'][bandname] for feature in fc]
  
def getX(fc, varname):
  """
  all other time series from feature collection
  """
  return [feature['properties'][varname] for feature in fc]

def rgb_to_hsv(r,g,b):  
  """
  convert r,g,b lists to h,s,v lists
  """
  rgb = list(zip(r,g,b))
  hsv = [colorsys.rgb_to_hsv(x[0],x[1],x[2]) \
    if (x[0] and x[1] and x[2]) and np.min(x) >= 0 and np.max(x[1]) <= 1 \
    else np.repeat(np.NaN,3) for x in rgb]
  return ([x[0] for x in hsv], [x[1] for x in hsv], [x[2] for x in hsv])

def lake_statistics_from_GeoJSON(base_path, target):
  """
  read lake statistics from geojson
  """
  
  fpaths = sorted(glob.glob(base_path+'*.geojson'))
  
  lake_statistics = []
  
  for fpath in fpaths:
    
    # feature collection (clean)
    fc = json.load(open(fpath))['features']  
    #fc = remove_baddies(fc, target)
    
    date = [datetime.datetime.utcfromtimestamp(x['properties']['timestamp']) for x in fc]
    fileID = getX(fc, 'fileID')
    
    b = getSR(fc, 'blue')
    g = getSR(fc, 'green')
    r = getSR(fc, 'red')
    n = getSR(fc, 'nir')
    s1 = getSR(fc, 'swir1')
    s2 = getSR(fc, 'swir2')
    
    h, s, v = rgb_to_hsv(r, g, b)
    
    BT_lake = getX(fc, 'BT_lake')
    BT_bkgd = getX(fc, 'BT_bkgd')
    dBT = [x[0]-x[1] if not None in x else None for x in list(zip(BT_lake,BT_bkgd))]
    
    cloud_count = getX(fc, 'cloud_count')
    water_count = getX(fc, 'water_count')
    sulphur_count = getX(fc, 'sulphur_count')
    
    lake_statistics.append((date, fileID, b, g, r, n, s1, s2, h, s, v, \
    BT_lake, BT_bkgd, dBT, cloud_count, water_count, sulphur_count))
  
  return lake_statistics

def build_DataFrame(lake_stats):
  
  df = pd.DataFrame({
  'datetime':list(itertools.chain(*[x[0] for x in lake_stats])),
  'fileID':list(itertools.chain(*[x[1] for x in lake_stats])),
  'blue' :list(itertools.chain(*[x[2] for x in lake_stats])),
  'green':list(itertools.chain(*[x[3] for x in lake_stats])),
  'red'  :list(itertools.chain(*[x[4] for x in lake_stats])),
  'nir'  :list(itertools.chain(*[x[5] for x in lake_stats])),
  'swir1':list(itertools.chain(*[x[6] for x in lake_stats])),
  'swir2':list(itertools.chain(*[x[7] for x in lake_stats])),
  'hue':list(itertools.chain(*[x[8] for x in lake_stats])),
  'saturation':list(itertools.chain(*[x[9] for x in lake_stats])),
  'value':list(itertools.chain(*[x[10] for x in lake_stats])),
  'BT_lake':list(itertools.chain(*[x[11] for x in lake_stats])),
  'BT_bkgd':list(itertools.chain(*[x[12] for x in lake_stats])),
  'dBT':list(itertools.chain(*[x[13] for x in lake_stats])),
  'cloud_count':list(itertools.chain(*[x[14] for x in lake_stats])),
  'water_count':list(itertools.chain(*[x[15] for x in lake_stats])),
  'sulphur_count':list(itertools.chain(*[x[16] for x in lake_stats])),
  })
  
  df.sort_values('datetime', inplace=True)

  return df

def DateFrame_to_Excel(df, target):
  """
  Pandas DataFrame to Microsoft Excel file
  """
  
  outdir = '/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/'+target
  if not os.path.exists(outdir): os.mkdir(outdir)
  os.chdir(outdir)
  
  writer = pd.ExcelWriter(target+'_satellite.xlsx')#target+'_satellite.xlsx'
  df.to_excel(writer,columns=\
  ['datetime','fileID','blue', 'green', 'red', 'nir', 'swir1', 'swir2',\
  'hue', 'saturation', 'value', 'BT_lake', 'BT_bkgd', 'dBT',\
  'cloud_count', 'water_count', 'sulphur_count'])
  
  writer.save()
  print(outdir)

def main():
  
  args = sys.argv[1:]

  if len(args) != 1:
    print('usage: python3 lakes_to_EXCEL.py {target_name}')
    return

  target = args[0]
  base_path = '/home/sam/git/crater_lakes/atmcorr/v2/lake_statistics/{}/'.format(target)
  lake_stats = lake_statistics_from_GeoJSON(base_path,target)
  df = build_DataFrame(lake_stats)
  DateFrame_to_Excel(df, target)

if __name__ == '__main__':
  main()