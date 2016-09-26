import gdal
import numpy as np
import matplotlib.pylab as plt
import sys


def display_doy(doy):
  
  if doy < 1 or doy > 366:
    print('day of year must be between 1 and 366')
    return
  
  # open geotiff
  ds = gdal.Open('ozone_fill_stack.tif')
  
  # convert to numpy array
  arr = np.array(ds.GetRasterBand(doy).ReadAsArray())
  
  # handle NaNs
  good = np.where(arr==arr)
  nan  = np.where(arr!=arr)
  if len(nan) == 2:
    arr[nan] = np.min(arr[good])
   
  # display image
  plt.imshow(arr)
  plt.title('Ozone Fill for doy = '+str(doy))
  plt.show()
  
  # stats
  print('min ozone: {:.2f} DU'.format(np.min(arr)))
  print('max ozone: {:.2f} DU'.format(np.max(arr)))
  

def main():
  
  args = sys.argv[1:]
  
  if len(args) != 1:
    print('usage: $ python3 ozone_fill_display.py doy')
    sys.exit(1)
  
  # select a day of year (i.e. 1-366)
  doy = args[0]
  
  # display this doy
  display_doy(int(doy))
  

if __name__ == '__main__':
  main()