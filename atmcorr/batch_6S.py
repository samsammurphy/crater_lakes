import pandas as pd
import datetime
from Py6S import *


df = pd.read_csv('/home/sam/git/crater_lakes/atmcorr/atmospheric_variables.csv')

for i in len(df.index):

	d = df.iloc()[i]

	fileID = d['system:index'].split('_')[-1]
    date = datetime.datetime.strptime(d['datetime'],'%Y-%m-%dT%H:%M:%S')
    
    # 6S object
    s = SixS()

    # aot = d.AOT 
    # o3 = d.O3 
    # etc..

