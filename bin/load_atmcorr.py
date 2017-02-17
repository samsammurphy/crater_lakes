#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
load_atmcorr.py, Sam Murphy (2017-02-02)

Loads atmospheric correction results for all satellites in chronological order

"""

import pickle
import itertools
import datetime
import numpy as np


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


#def load_plot_data(target):
#  """
#  Handle missing blue, clip rgb between 0 and 1, save to dictionary
#  """
#  
#  # load data in chronological order
#  data = chronological_data(target)
#  
#  # create lists
#  r = []
#  g = []
#  b = []
#  dT = []
#  timestamps = []
#  satellites = []
#
#  # avoid None blue, and clip rgb
#  for d in data:
#    if d['sr']['blue']:
#      r.append(np.clip(d['sr']['red'],0,1))
#      g.append(np.clip(d['sr']['green'],0,1))
#      b.append(np.clip(d['sr']['blue'],0,1))
#      dT.append(d['T']['dBT'])
#      timestamps.append(d['timestamp'])
#      satellites.append(d['satellite'])
#
#  return {
#      'r':r,
#      'g':g,
#      'b':b,
#      'dT':dT,
#      'timestamps':timestamps,
#      'datetimes':[datetime.datetime.fromtimestamp(t) for t in timestamps],    
#      'satellites':satellites
#      }
#  