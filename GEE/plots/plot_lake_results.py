import datetime
from load_results import load_results
from matplotlib import pylab as plt

def shared_plot_characteristics(ax):
  # legend
  box = ax.get_position()
  ax.set_position([box.x0, box.y0, box.width * 0.85, box.height])
  ax.legend(loc='center left', bbox_to_anchor=(1,0.5),shadow=True,fancybox=True)
  # x-axis
  ax.set_xlim(datetime.datetime(1990,1,1),datetime.datetime(2016,1,1))
  # grid 
  ax.grid()

def subplot_vis(ax,vswir):
  ax.plot(vswir['date'],vswir['red'],'red',label='red')
  ax.plot(vswir['date'],vswir['green'],'green',label='green')
  ax.plot(vswir['date'],vswir['blue'],'blue',label='blue')
  ax.set_ylabel('surface reflectance')
  ax.set_ylim(0,0.5) 
  shared_plot_characteristics(ax)
  
def subplot_value_sat(ax,vswir):
  ax.plot(vswir['date'],vswir['value'],'black', label = 'value')
  ax.plot(vswir['date'],vswir['saturation'],'gray', label = 'saturation')
  ax.set_ylabel('surface reflectance')
  ax.set_ylim(0,0.5)
  shared_plot_characteristics(ax)
  
def subplot_temperature(ax,tir):
  ax.plot(tir['date'],tir['dT'],'red', label = '$\Delta$T')
  ax.set_ylabel(r"$\Delta$T ($^\circ$C)")
  ax.set_ylim(0,30)
  shared_plot_characteristics(ax)

def subplot_size(ax,count):
  #ax.plot(count['date'],count['lake_count']+count['cloud_count'],'green',label='lake+cloud')
  ax.plot(count['date'],count['lake_size'],'blue',label='lake')
  ax.plot(count['date'],count['cloud_size'],'grey',label='cloud')
  ax.set_ylabel(r"area (m$^2$)")
  ax.get_yaxis().set_major_formatter(plt.LogFormatter(10,  labelOnlyBase=False))
  shared_plot_characteristics(ax)

def plot_main():
  
  target = 'Poas'
  data = load_results(target)
  
  f, (ax1, ax2, ax3, ax4) = plt.subplots(4,1, sharex=True)# 4 subplots in 1 column (share x-axis)
  subplot_vis(ax1,data['vswir'])
  subplot_value_sat(ax2,data['vswir'])
  subplot_temperature(ax3,data['tir'])
  subplot_size(ax4,data['count'])

plot_main()
  