import Quandl
import numpy as np
import pandas as pd
import pylab
import matplotlib.pyplot as plt
import datetime
import pdb

TOKEN = "HtX8WxoywJDWHYiy4qzP"
pd.options.display.mpl_style = 'default'

print 'Pandas Version', pd.__version__
print 'Numpy Version', np.__version__

#pd.DataFrame(np.random.randn(120,10).cumsum(axis=0)).plot(title='Brownian Motion')
#pylab.show(block = True)

goldPrice = Quandl.get("BUNDESBANK/BBK01_WT5511", trim_start="1968-04-01", trim_end="2014-07-18", authtoken="HtX8WxoywJDWHYiy4qzP", returns = "numpy")
USAGDP = Quandl.get("WORLDBANK/USA_NY_GDP_MKTP_CN", trim_start="1960-12-31", trim_end="2012-12-31", authtoken="HtX8WxoywJDWHYiy4qzP", collapse="annual", returns = "numpy")


#dimensions of the dataframe
goldPrice.ndim
USAGDP.ndim


# df = USAGDP

# #Show the first few rows of the dataframe
# df.head(5)
# df.head(11)

# #show the last few
# df.tail()

# #drop rows with missing data
# df.dropna(how = 'any')

# #Fill missing data
# df.fillna(value = 123)

# #get the boolean mask where values are nan
# pd.isnull(df)



pdb.set_trace()

fig1 = plt.figure(1, figsize = [8,6])
ax1 = fig1.add_subplot(111)
plt.plot(goldPrice)
plt.plot(USAGDP)

pylab.show(block = True)