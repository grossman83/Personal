import Quandl
import numpy as np
import pylab
import matplotlib as mpl
import matplotlib.pyplot as plt
import datetime
import pdb
import h5py as h5


#Get data from Quandl and store it for later use.
TOKEN = "HtX8WxoywJDWHYiy4qzP"

f = h5.File('wti.h5', 'w')


wti = Quandl.get("FRED/DCOILWTICO", trim_start="2015-03-01", authtoken = TOKEN, returns = "numpy")
uwti = Quandl.get("GOOG/NYSEARCA_UWTI", trim_start = "2015-03-01", authtoken = TOKEN, returns = "numpy")

# pdb.set_trace()



fig1 = plt.figure(1, figsize = [12, 8])
ax1 = fig1.add_subplot(111)
p1 = plt.plot_date(mpl.dates.date2num(wti.Date), wti.Value/wti.Value[0], 'r')
p2 = plt.plot_date(mpl.dates.date2num(uwti.Date), uwti.Close/uwti.Close[0], 'b')
#these two have different lengths and need to be tweaked.
# p3 = plt.plot_date(mpl.dates.date2num(uwti.Date), (uwti.Close/uwti.Close[0])/(wti.Value/wti.Value[0]), 'g')

pylab.show()




print np.shape(wti)
print wti.date