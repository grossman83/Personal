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

f = h5.File('QuandlNumbers1.h5', 'w')

goldPrice = Quandl.get("BUNDESBANK/BBK01_WT5511", trim_start="1968-04-01", trim_end="2014-07-18", authtoken="HtX8WxoywJDWHYiy4qzP", returns = "numpy")
f['goldPrice'] = [matplotlib.dates.date2num(goldPrice.Date), goldPrice.Value]

USAGDP = Quandl.get("WORLDBANK/USA_NY_GDP_MKTP_CN", trim_start="1960-12-31", trim_end="2012-12-31", authtoken="HtX8WxoywJDWHYiy4qzP", collapse="annual", returns = "numpy")
f['USAGDP'] = [matplotlib.dates.date2num(USAGDP.Date), USAGDP.Value]

CAHomeOwnership = Quandl.get("FRED/CAHOWN", trim_start="1984-01-01", trim_end="2012-01-01", collapse="annual", returns = "numpy")
f['CAHomeOwnership'] = [matplotlib.dates.date2num(CAHomeOwnership.Date), CAHomeOwnership.Value]

CAHomePriceIndex = Quandl.get("FRED/CASTHPI", trim_start="1975-01-01", trim_end="2014-01-01", collapse="quarterly", returns = "numpy")
f['CAHomePriceIndex'] = [matplotlib.dates.date2num(CAHomePriceIndex.Date), CAHomePriceIndex.Value]

RealGDPPerCapitaUS = Quandl.get("FRED/USARGDPC", trim_start="1960-01-01", trim_end="2011-01-01", collapse="annual", returns = "numpy")
f['RealGDPPerCapitaUS'] = [matplotlib.dates.date2num(RealGDPPerCapitaUS.Date), RealGDPPerCapitaUS.Value]

SP500 = Quandl.get("YAHOO/INDEX_GSPC", trim_start="1950-01-03", trim_end="2014-07-22", returns = "numpy")
f['SP500'] = [matplotlib.dates.date2num(SP500.Date), SP500.Open, SP500.High, SP500.Low, SP500.Close]

NASDAQ = Quandl.get("YAHOO/INDEX_IXIC", trim_start="1971-02-05", trim_end="2014-07-22", returns = "numpy")
f['NASDAQ'] = [matplotlib.dates.date2num(NASDAQ.Date), NASDAQ.Close]

DowJones = Quandl.get("BCB/UDJIAD1", trim_start="1896-07-14", trim_end="2014-07-22", returns = "numpy")
f['DowJones'] = [matplotlib.dates.date2num(DowJones.Date), DowJones.Value]

NIKKEI225 = Quandl.get("YAHOO/INDEX_N225", trim_start="1950-01-04", trim_end="2014-07-21", returns = "numpy")
f['NIKKEI225'] = [matplotlib.dates.date2num(NIKKEI225.Date), NIKKEI225.Close]

JPNRealGDPPerCapita = Quandl.get("ODA/JPN_PPPPC", trim_start="1980-12-31", trim_end="2019-12-31", collapse="annual", returns = "numpy")
f['JPNRealGDPPerCapita'] = [matplotlib.dates.date2num(JPNRealGDPPerCapita.Date), JPNRealGDPPerCapita.Value]

USAUEMPMEAN = Quandl.get("FRED/UEMPMEAN", trim_start="1948-01-01", trim_end="2014-06-01", collapse="monthly", returns = "numpy")
f['USAUEMPMEAN'] = [matplotlib.dates.date2num(USAUEMPMEAN.Date), USAUEMPMEAN.Value]

USACUnempRatio = Quandl.get("FRED/EMRATIO", trim_start="1948-01-01", trim_end="2014-06-01", collapse="monthly", returns = "numpy")
f['USACUnempRatio'] = [matplotlib.dates.date2num(USACUnempRatio.Date), USACUnempRatio.Value]

JPNInflation = Quandl.get("WORLDBANK/JPN_FP_CPI_TOTL_ZG", trim_start="1961-12-31", trim_end="2013-12-31", collapse="annual", returns = "numpy")
f['JPNInflation'] = [matplotlib.dates.date2num(JPNInflation.Date), JPNInflation.Value]

NIKKEI = Quandl.get("NIKKEI/INDEX", trim_start="1950-01-04", trim_end="2014-07-22", returns = "numpy")
f['NIKKEI'] = [matplotlib.dates.date2num(NIKKEI.Date), NIKKEI['Open Price'], NIKKEI['Close Price']]

USAInflation = Quandl.get("WORLDBANK/USA_FP_CPI_TOTL_ZG", trim_start="1961-12-31", trim_end="2012-12-31", collapse="annual", returns = "numpy")
f['USAInflation'] = [matplotlib.dates.date2num(USAInflation.Date), USAInflation.Value]






#pdb.set_trace()




















