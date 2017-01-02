"""

Landsat and ASTER plot

- spectral and spatial comparison

"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# draws a box on a plot
def draw_box(ax, x,y,dx,dy,color):
  ax.add_patch(patches.Rectangle((x,y), dx, dy, 
                                  color=color,
                                  alpha=0.6,
                                  fill=True,
                                  linewidth=2))
  
def draw_mission(ax, satellite, ypos):
  bandNames = sorted(satellite.keys())
  for bandName in bandNames:
    waveband = satellite[bandName]
    xpos = waveband[0]
    dx = waveband[1]-waveband[0]
    dy = 0.5
    draw_box(ax, xpos,ypos,dx,dy,waveband[2])
    
def draw_missions(ax, satellites):
  for count, satellite in enumerate(satellites):
    ypos = count + 0.75
    draw_mission(ax, satellite, ypos)

def NASA_visible_wavelengths(ax1):
  """
  https://en.wikipedia.org/wiki/Color
  """
  B = 0.475
  G = 0.540
  R = 0.665
  
  
  ax1.axvspan(B,B,color='blue',linestyle='--')
  ax1.axvspan(G,G,color='green',linestyle='--')
  ax1.axvspan(R,R,color='red',linestyle='--')

# satellite wavebands 
TM = {
  'B1': (0.43, 0.56,'blue') ,'B2': (0.5, 0.65,'green'),'B3': (0.58, 0.74,'red'),
  'B4': (0.73, 0.95,'violet'),'B5': (1.5025, 1.89,'black'),'B6': (10.4,12.5,'black'),
  'B7': (1.95, 2.41,'black')
}

ETM = {
  'B1': (0.435, 0.52, 'blue'),'B2': (0.5, 0.6225,'green'),'B3': (0.615, 0.7025,'red'),
  'B4': (0.74, 0.9125,'violet'),'B5': (1.51, 1.7875,'black'),'B6': (10.4,12.5,'black'),
  'B7': (2.015, 2.3775,'black')
}


OLI = {
  'B1': (0.427, 0.457,'blue'),'B2': (0.436, 0.526,'blue'),'B3': (0.512, 0.61,'green'),
  'B4': (0.625, 0.69,'red'),'B5': (0.829, 0.899,'violet'),'B6': (1.515, 1.695,'black'),
  'B7': (2.037, 2.354,'black'),'B9': (1.34, 1.407,'black'),'B10':(10.3,11.3,'black'),
  'B11':(11.5,12.5,'black')# 'PAN': (0.488, 0.691,'black')
}

AST = {
  'B1': (0.485, 0.6425, 'green'),'B2': (0.59, 0.73, 'red'),'B3B':(0.72, 0.9225,'violet'),
  'B3N':(0.72, 0.9075,'violet'),'B4': (1.57, 1.7675,'black'),'B5': (2.12, 2.2825,'black'),
  'B6': (2.15, 2.295,'black'),'B7': (2.21, 2.39,'black'),'B8': (2.25, 2.244,'black'),
  'B9': (2.2975, 2.4875,'black'),'B10': (8.125,8.475,'black'),'B11': (8.475,8.825,'black'),
  'B12': (8.925,9.275,'black'),'B13': (10.25,10.95,'black'),'B14': (10.95,11.65,'black')
}

satellites = [TM,ETM,OLI,AST]

# Figure space
fig = plt.figure(figsize=(16,10))
ysize = 0.28      # normalized y size of each graph
dy = (1-3*ysize)/4


# VNIR
ax1 = fig.add_axes([0.05, ysize*2 + 3*dy, 0.9, ysize])
ax1.set_xlim(0.4,1)
ax1.set_ylim(0,5)
ax1.set_yticks([0,1,2,3,4,5],['','TM','ETM+','OLI/TIRS','ASTER',''])
#NASA_visible_wavelengths(ax1)
draw_missions(ax1, satellites)

# SWIR
ax2 = fig.add_axes([0.05, ysize*1 + 2*dy, 0.9, ysize])
ax2.set_xlim(1,3)
ax2.set_ylim(0,5)
draw_missions(ax2, satellites)

# TIR
ax3 = fig.add_axes([0.05, dy, 0.9, ysize])
ax3.set_xlim(8,13)
ax3.set_ylim(0,5)
draw_missions(ax3, satellites)

fig.show()