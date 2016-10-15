"""
Converts a GEE geometry to a KML polygon

Linear rings - only

"""


# convert geom to kml
def geom_to_kml(geom_string):
  """
  Removes brackets '[]' (i.e. not used in kml)
  and add a z component (i.e. ,0.0)
  note kml coords are: x1,y1,z1 x2,y2,z2 .. (i.e. coords separated by whitespace)
  """
  # coords string  
  gee_coords_string = geom[:-1].split('(')[1][1:-1]
  # remove '[' 
  bracket_removed = gee_coords_string.replace('[','')
  # replace ']' with '0.0' to get a kml coords string (i.e. add z component)
  kml_coords_string = bracket_removed.replace('],',',0.0 ')
  # kml container
  kml_prefix = '<Polygon><outerBoundaryIs><LinearRing><coordinates>'
  kml_suffix = '</coordinates></LinearRing></outerBoundaryIs></Polygon>'
  
  return kml_prefix+kml_coords_string+kml_suffix



# Google Earth Engine geometry string
geom = 'ee.Geometry.LinearRing([[167.82157, -15.38674],[167.82938, -15.38294],[167.83908, -15.386],[167.84174, -15.39237],[167.840195, -15.395349],[167.82706, -15.39767],[167.82389, -15.39659],[167.82045, -15.38972]])'
geom = 'ee.Geometry.LinearRing([[167.81118, -15.40884135660561], [167.86045, -15.40884135660561], [167.86045, -15.373249999999977], [167.81118, -15.373249999999977], [167.81118, -15.40884135660561]])'

# KML polygon
kml = geom_to_kml(geom)

print(kml)


#<Polygon><outerBoundaryIs><LinearRing><coordinates>167.82157, -15.38674,0.0,167.82938, -15.38294,0.0,167.83908, -15.386,0.0,167.84174, -15.39237,0.0,167.840195, -15.395349,0.0,167.82706, -15.39767,0.0,167.82389, -15.39659,0.0,167.82045, -15.38972,0.0</coordinates></LinearRing></outerBoundaryIs></Polygon>
#<Polygon><outerBoundaryIs><LinearRing><coordinates>167.820079,-15.382608,0.0 167.820097,-15.403755,0.0 167.858821,-15.404158,0.0 167.859552,-15.38298,0.0 167.820079,-15.382608,0.0</coordinates></LinearRing></outerBoundaryIs></Polygon>