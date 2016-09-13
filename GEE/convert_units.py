
  
# function to convert H2O units (Google = kg/m^2, Py6S = g/cm^2)
def convert_H2O_units(H2O_google):
  return float(H2O_google) * 1000 / 10000 #(i.e. kg to g multiple by 1000, 1/m2 to 1/cm2 divide by 10000)

# function to convert O3 units (Google = Dobson Units, Py6S = atm-cm)
def convert_O3_units(O3_google):
  return float(O3_google) / 1000 # (i.e. Dobson units are milli-atm-cm )

