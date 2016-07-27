# -*- coding: utf-8 -*-
"""

Plot lake colour and temperature time series


"""

import os
import csv
from matplotlib import pyplot as plt
import numpy as np

# get decimal year from filename
def dyear(filename):
  year = float(filename[9:13])
  doy = float(filename[13:16])
  return year + doy/365
  
# read csv to 'decimal_year' and 'value' lists
def readTimeSeries(filename):
  # read csv file to lists
  decimal_year = []
  value = []
  with open(filename, 'r') as csvfile:
    rownum = 0
    reader = csv.reader(csvfile)
    for row in reader:
      if rownum != 0:# avoid header
        value_str = (((row[1].split('='))[1]).split('}'))[0]
        if value_str != 'null':   
          decimal_year.append(dyear(row[0]))
          value.append(float(value_str))
      rownum += 1
  
  # sort data (avoid weird line plots)
  sorted_dyear  = [x for (x,y) in sorted(zip(decimal_year,value))]
  sorted_value = [y for (x,y) in sorted(zip(decimal_year,value))]
  
  return [sorted_dyear,sorted_value]

  
# working directory
volcano_name = 'Taupo'
os.chdir('/home/sam/0_Crater_Lakes/z/2016-06-17_NASA_report_material/3)_Time_series/'+volcano_name)
  
# time series
colour = readTimeSeries('NDCI_'+volcano_name+'.csv')
temperature = readTimeSeries('temperature_'+volcano_name+'.csv')

# colour plot
plt.xlim([2000,2016])
plt.plot(colour[0],colour[1], color='b')
plt.xlabel('Year', fontsize=18)
plt.ylabel('NDCI', fontsize=16)
plt.show()

# temperature plot
plt.xlim([2000,2016])
plt.plot(temperature[0],np.array(temperature[1])-273, color='r')
plt.xlabel('Year', fontsize=18)
plt.ylabel('Lake Temperature (oC)', fontsize=16)
plt.show()

