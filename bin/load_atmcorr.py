#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
load_atmcorr.py, Sam Murphy (2017-02-02)

Loads atmospheric correction results for all satellites in chronological order

"""

import pickle
import itertools


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
