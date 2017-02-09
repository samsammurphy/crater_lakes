#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

compare_HSV_to_SV, Sam Murphy (2016-11-07)


"""

import colorsys
from load_results import load_results
from matplotlib import pylab as plt
from mpldatacursor import datacursor


def modified_HSV(r,g):
  """
  returns 'saturation' and 'value' of green-red color space
  """
  mx = max(r,g)
  mn = min(r,g) 
  df = mx-mn
  s = df/mx
  v = mx
  
  # must be between 0 and 1
  s = max(min(s, 1), 0)
  v = max(min(v, 1), 0)
  return(s,v)

def saturation_value(r,g,b):
  """
  returns 'saturation' and 'value' for i) normal HSV and ii) modified HSV
  """
  saturation = []
  value = []
  for i in range(len(b)):    
    # normal HSV
    HSV = colorsys.rgb_to_hsv(r[i],g[i],b[i])
    # modified SV
    sv = modified_HSV(r[i],g[i])
    # jobs a goodun
    saturation.append((HSV[1],sv[0]))
    value.append((HSV[2],sv[1]))
  return(saturation, value)
  
def plot(r,g,b,saturation,value,date):
  """
  plots i) RGB, ii) saturation, iii) value
  """
  f, (ax1, ax2, ax3) = plt.subplots(3,1, sharex=True)
  # visible RGB
  ax1.plot(date,r,'-r',label='red')
  ax1.plot(date,g,'-g',label='green')
  ax1.plot(date,b,'-b',label='blue')
  ax1.set_ylabel('rho')
  # saturation compare
  S = [sat1 for (sat1,sat2) in saturation]
  s = [sat2 for (sat1,sat2) in saturation]       
  ax2.plot(date,S,'.r',label='HSV_sat')
  ax2.plot(date,s,'.g',label='SV_sat')
  ax2.set_ylabel('sat.')
  # value compare
  V = [v1 for (v1,v2) in value]
  v = [v2 for (v1,v2) in value]       
  ax3.plot(date,V,'.r',label='HSV_value')
  ax3.plot(date,v,'.g',label='SV_value')
  ax3.set_ylabel('value')

def main():
  # read the data
  target = 'Crater_Lake'
  vswir = (load_results(target))['vswir']
  r,g,b = vswir['red'],vswir['green'],vswir['blue']
  saturation, value = saturation_value(r,g,b)
  plot(r,g,b,saturation,value,vswir['date'])
  # interact with data
  datacursor()
  
if __name__ == '__main__':
  main()