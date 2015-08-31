import Quandl
import numpy as np
import pylab
import matplotlib
import matplotlib.pyplot as plt
import datetime
import pdb
import h5py as h5

TOKEN = "HtX8WxoywJDWHYiy4qzP"



USAGGRvGDP = Quandl.get("ODA/USA_GGR_NGDP", trim_start="1980-12-31", trim_end="2019-12-31", authtoken="HtX8WxoywJDWHYiy4qzP", collapse="annual", returns = "numpy")
USAGGSvGDP = Quandl.get("ODA/USA_GGX_NGDP", trim_start="1980-12-31", trim_end="2019-12-30", authtoken="HtX8WxoywJDWHYiy4qzP", collapse="annual", returns = "numpy")

fig1 = plt.figure(1, figsize = [12,9])
ax1 = fig1.add_subplot(111)
p1 = plt.plot(USAGGRvGDP.Date, USAGGRvGDP.value)
p2 = plt.plot(USAGGSvGDP.Date, USAGGSvGDP.value)

pylab.show()