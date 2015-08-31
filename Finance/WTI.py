import Quandl
import numpy as np
import pylab
import matplotlib
import matplotlib.pyplot as plt
import datetime
import pdb
import h5py as h5


#Get data from Quandl and store it for later use.
TOKEN = "HtX8WxoywJDWHYiy4qzP"

f = h5.File('wti.h5', 'w')


wti = Quandl.get("WSJ/OIL_WTI", trim_start="2012-06-01", authtoken = TOKEN, returns = "numpy")
uwti = Quandl.get("GOOG/NYSEARCA_UWTI", trim_start = "2012-06-01", authtoken = TOKEN, returns = "numpy")

# pdb.set_trace()

fig1 = plt.figure(1, figsize = [12, 8])
ax1 = fig1.add_subplot(111)
p1 = plt.plot_date(wti.Date, wti.Value)
p2 = plt.plot_date(uwti.Date, uwti.Close)

pylab.show()




print np.shape(wti)
print wti.date