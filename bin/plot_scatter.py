#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

plot_scatter.py

Created on Tue Feb 14 15:53:13 2017

@author: sam
"""

import pandas as pd
import numpy as np
import matplotlib.pylab as plt

def null_handler(x,y,df):
  """
  Handle null values, only return good values
  """
  x_ok = np.array([~pd.isnull(df[x])])[0]
  y_ok = np.array([~pd.isnull(df[y])])[0]
  ok = x_ok * y_ok
  
  return (df[x][ok],df[y][ok])

def main():
  
  x = 'K'
  y = 'SO4'
  df = pd.read_excel('/home/sam/Dropbox/HIGP/Crater_Lakes/Dmitri_Sam/data/Yugama/Yugama.xlsx')
  
  good = null_handler(x,y,df)
  
  plt.plot(good[0],good[1],'*')
  plt.xlabel(x)
  plt.ylabel(y)

"""
Correlations include:
  
  Cl, pH
  Cl, Al
  Fe, Ca
  
"""

if __name__ == '__main__':
  main()