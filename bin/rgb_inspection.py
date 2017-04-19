import numpy as np

def rgb_stretch(R,G,B, top):
  """
  Linear stretch of R, G, B and zip together, 
  """

  R = np.clip(R/top,0,1)
  G = np.clip(G/top,0,1)
  B = np.clip(B/top,0,1)
  return (R,G,B)


# b = 0.0341458205	
# g = 0.0334175792	
# r = 0.0366226966

# b = 0.0268601052	
# g = 0.0269842867	
# r = 0.02752911

# b = 0.0407537061	
# g = 0.0434961468	
# r = 0.0473292466

# 2013-01-15
b = 0.0700247203	
g = 0.0763519408
r =	0.087073169



rgb = (r,g,b)
top = 0.15

stretched_rgb = rgb_stretch(rgb[0],rgb[1],rgb[2],top)

print('original rgb = ',rgb)
print('strecthed rgb = {0[0]:.6f}, {0[1]:.6f}, {0[2]:.6f}'.format(stretched_rgb))

