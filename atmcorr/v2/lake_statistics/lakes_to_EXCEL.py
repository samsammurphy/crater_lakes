
import glob
import json
import itertools

#Extracts surface reflectance time series from feature collection
def SR_from_FC(feature_collection,bandname):return [feature['properties']['lake_average'][bandname] for feature in feature_collection]

base_path = '/home/sam/git/crater_lakes/atmcorr/v2/lake_averages/Kelimutu_b/'
fpaths = sorted(glob.glob(base_path+'*.geojson'))

lake_averages = []

for fpath in fpaths:

    feature_collection = json.load(open(fpath))['features']  
    b = SR_from_FC(feature_collection,'blue')
    g = SR_from_FC(feature_collection,'green')
    r = SR_from_FC(feature_collection,'red')
    n = SR_from_FC(feature_collection,'nir')
    s1 = SR_from_FC(feature_collection,'swir1')
    s2 = SR_from_FC(feature_collection,'swir2')

    lake_averages.append((b,g,r,n,s1,s2))

blue  = list(itertools.chain(*[x[0] for x in lake_averages]))
green = list(itertools.chain(*[x[1] for x in lake_averages]))
red   = list(itertools.chain(*[x[2] for x in lake_averages]))
nir   = list(itertools.chain(*[x[3] for x in lake_averages]))
swir1 = list(itertools.chain(*[x[4] for x in lake_averages]))
swir2 = list(itertools.chain(*[x[5] for x in lake_averages]))

