# -*- coding: utf-8 -*-
"""

Plot lake temperature time series


"""

import os
import csv
from matplotlib import pyplot as plt

#get decimal year from filename
def dyear(filename):
  year = float(filename[9:13])
  doy = float(filename[13:16])
  return year + doy/365
  

# working directory
os.chdir('/home/sam/0_Crater_Lakes/z/2016-06-17_NASA_report_material/3)_Time_series/')

# read csv file to lists
fileIDs = []
decimal_year = []
temperature = []
with open('temperature_Ruapehu.csv', 'r') as csvfile:
  rownum = 0
  reader = csv.reader(csvfile)
  for row in reader:
    if rownum != 0:               # avoid header
      BT_str = (((row[1].split('='))[1]).split('}'))[0]
      if BT_str != 'null':        #ignore null values (i.e. cloudy lakes)
        fileIDs.append(row[0])  
        decimal_year.append(dyear(row[0]))
        temperature.append(float(BT_str))
    rownum += 1

# sort data (avoid weird line plots)
sorted_dyear  = [x for (x,y) in sorted(zip(decimal_year,temperature))]
sorted_temp = [y for (x,y) in sorted(zip(decimal_year,temperature))]

# plot the data
plt.plot(sorted_dyear,sorted_temp)