#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_test.py
"""

import pickle
import datetime

from matplotlib import pylab as plt


def plot_sr(data,name,symbol):
  """
  Plots a given surface reflectance variable (e.g. blue) by name. 
  """
  date = [datetime.datetime.fromtimestamp(d['timestamp']) for d in data if name in d['sr']]
  value = [d['sr'][name] for d in data if name in d['sr']]
  
  variable_colour = {
                    'blue':'b',
                    'green':'g',
                    'red':'r'
                    }
  
  colour = variable_colour[name]              
                    
  plt.plot(date,value,colour+symbol)


def satellite_plot(base_path,target,satellite):

  with open('{}{}_{}.p'.format(base_path,target,satellite),"rb") as f:
    data = pickle.load(f)
    
  satellite_symbol = {
                      'L4':'s',
                      'L5':'s',
                      'L7':'s',
                      'L8':'s',
                      'AST':'s',
                      }
  
  symbol = satellite_symbol[satellite]
  
  plot_sr(data,'blue',symbol)


def main():
  
  target = 'Aoba'
  
  base_path = '/home/sam/git/crater_lakes/atmcorr/results/{}/'.format(target)

  satellite = 'L7'
  
  # define a plot space
  
  # plot each satellite in turn (unique symbol for each satellite)
  satellite_plot(base_path,target,satellite)
  

if __name__ == '__main__':
  main()  