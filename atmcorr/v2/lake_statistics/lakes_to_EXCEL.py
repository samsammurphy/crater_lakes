
import glob
import json
import itertools

# surface reflectance time series from feature collection
def SR_from_FC(feature_collection,bandname):return [feature['properties']['lake_SR'][bandname] for feature in feature_collection]

# all other time series from feature collection
def X_from_FC(feature_collection, varname): return [feature['properties'][varname] for feature in feature_collection]

base_path = '/home/sam/git/crater_lakes/atmcorr/v2/lake_statistics/Kelimutu_b/'
fpaths = sorted(glob.glob(base_path+'*.geojson'))

lake_statistics = []

for fpath in fpaths:

    feature_collection = json.load(open(fpath))['features']  
  
    b = SR_from_FC(feature_collection,'blue')
    g = SR_from_FC(feature_collection,'green')
    r = SR_from_FC(feature_collection,'red')
    n = SR_from_FC(feature_collection,'nir')
    s1 = SR_from_FC(feature_collection,'swir1')
    s2 = SR_from_FC(feature_collection,'swir2')

    BT_lake = X_from_FC(feature_collection,'BT_lake')
    BT_bkgd = X_from_FC(feature_collection,'BT_bkgd')

    cloud_count = X_from_FC(feature_collection,'cloud_count')
    water_count = X_from_FC(feature_collection,'water_count')
    sulphur_count = X_from_FC(feature_collection,'sulphur_count')

    lake_statistics.append((b,g,r,n,s1,s2,BT_lake,BT_bkgd,cloud_count,water_count,sulphur_count))

blue  = list(itertools.chain(*[x[0] for x in lake_statistics]))
green = list(itertools.chain(*[x[1] for x in lake_statistics]))
red   = list(itertools.chain(*[x[2] for x in lake_statistics]))
nir   = list(itertools.chain(*[x[3] for x in lake_statistics]))
swir1 = list(itertools.chain(*[x[4] for x in lake_statistics]))
swir2 = list(itertools.chain(*[x[5] for x in lake_statistics]))

BT_lake = list(itertools.chain(*[x[6] for x in lake_statistics]))
BT_bkgd = list(itertools.chain(*[x[7] for x in lake_statistics]))

cloud_count = list(itertools.chain(*[x[8] for x in lake_statistics]))
water_count = list(itertools.chain(*[x[9] for x in lake_statistics]))
sulphur_count = list(itertools.chain(*[x[10] for x in lake_statistics]))