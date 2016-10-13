from load_results import load_results
from matplotlib import pylab as plt
from mpldatacursor import datacursor

  
#config
target = 'Aoba'
waveband = 'blue'

#load data
data = load_results(target)
refs = data['vswir']
LEDAPS = data['LEDAPS']
print('LEDAPS length = ',len(LEDAPS[waveband]))

# figure instance
fig = plt.figure()
fig.suptitle(target, fontsize=15)
plt.figtext(0.15,0.85,waveband, fontsize=12, ha='left')

# axes instance
ax = fig.add_subplot(1,1,1)
ax.set_ylabel('surface reflectance')
ax.set_xlabel('date')
ax.set_ylim(-2,2)

# plot data
ax.plot(refs['date'],refs[waveband],waveband,lw=2)
ax.plot(LEDAPS['date'],LEDAPS[waveband],'r',alpha=0.25)
ax.plot(LEDAPS['date'],LEDAPS[waveband],'.r')

# interactive with data
datacursor()







