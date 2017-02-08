#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
load_atmcorr.py, Sam Murphy (2017-02-02)

Loads atmospheric correction results for all satellites in chronological order

"""

import pickle
import itertools
import datetime


def chronological_data(target):
  """
  Loads all satellite data together and chronologically sorts
  """
  
  base_path = '/home/sam/git/crater_lakes/atmcorr/results/{}/'.format(target)
  
  def load_sat(sat): 
    fname = '{}{}_{}.p'.format(base_path,target,sat)
    data = pickle.load(open(fname,"rb"))
    return data
  
  # data for each satellite
  L4 = load_sat('L4')  
  L5 = load_sat('L5')  
  L7 = load_sat('L7')  
  L8 = load_sat('L8')  
  #AST = load_sat('AST')  
  
  # chain all satellites together
  data = list(itertools.chain(L4,L5,L7,L8))#,AST
  
  # sort by timestamp
  def timestamp(dictionary): return dictionary['timestamp']
  data = sorted(data,key=timestamp)
  
  return data


def load_plot_data(target):
  """
  Forces rgb to be between 0 and 1
  """
  data = chronological_data(target)   
  r = [sorted([0,d['sr']['red'],1])[1] for d in data]
  g = [sorted([0,d['sr']['green'],1])[1] for d in data]
  b = [sorted([0,d['sr']['blue'],1])[1] for d in data]
  dT = [d['T']['dBT'] for d in data]
  timestamps = [d['timestamp'] for d in data]   
  datetimes = [datetime.datetime.fromtimestamp(t) for t in timestamps]
  satellites = [d['satellite'] for d in data]
  
  return {
      'r':r,
      'g':g,
      'b':b,
      'dT':dT,
      'timestamps':timestamps,
      'datetimes':datetimes,    
      'satellites':satellites
      }
  