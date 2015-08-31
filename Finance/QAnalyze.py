import numpy as np
import pylab
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import h5py as h5




f = h5.File('QuandlNumbers1.h5', 'r')
goldPrice = f['goldPrice']
USAGDP = f['USAGDP']
SP500 = f['SP500']
NIKKEI = f['NIKKEI']
JPNRealGDPPerCapita = f['JPNRealGDPPerCapita']

# print(NIKKEI[2,:])

CAHomeOwnership = f['CAHomeOwnership']
RealGDPPerCapitaUS = f['RealGDPPerCapitaUS']
USAInflation = f['USAInflation']


fig1 = plt.figure(1, figsize = [12, 9])
ax1 = fig1.add_subplot(111)

print(goldPrice[0,:])

#p1 = plt.plot_date(mdates.num2date(goldPrice[0,:]), goldPrice[1,:] / max(goldPrice[1,:]), c = 'r')
#p2 = plt.plot_date(mdates.num2date(USAGDP[0,:]), USAGDP[1,:] / max(USAGDP[1,:]), c = 'g')
#p3 = plt.plot_date(mdates.num2date(RealGDPPerCapitaUS[0,:]), RealGDPPerCapitaUS[1,:])
#p4 = plt.plot_date(mdates.num2date(USAInflation[0,:]), USAInflation[1,:])
p5 = plt.plot_date(mdates.num2date(NIKKEI[0,:]), NIKKEI[2,:] / max(NIKKEI[2,:]), c = 'r')
# p6 = plt.plot_date(mdates.num2date(SP500[0,:]), SP500[4,:] / max(SP500[4,:]), c = 'r')
p7 = plt.plot_date(mdates.num2date(JPNRealGDPPerCapita[0,:]), JPNRealGDPPerCapita[1,:] / max(JPNRealGDPPerCapita[1,:]), c = 'b')


pylab.show()