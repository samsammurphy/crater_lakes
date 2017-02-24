#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

baddies.py

A place to store the bad image files found manually.

They will be removed AFTER atmospheric correction but BEFORE being saved
to excel file output.

Note > plots use the excel file


Created on Wed Feb 22 11:45:25 2017
@author: sam
"""



def naughty_list(target):
  
  bad_files = {
      
      'Kelimutu_c': ['LT51120662000004ASA00']
      
      }
      
  if target in bad_files.keys():
    
    return bad_files[target]
  
  else :
    
    return []
      

  
  
  
  
  