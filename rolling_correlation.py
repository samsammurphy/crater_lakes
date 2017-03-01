# -*- coding: utf-8 -*-
"""

rolling_correlation.py

This is a temporary script file.
"""

import numpy as np
import pandas as pd
import matplotlib.pylab as plt


# some data
a = np.random.randn(20)
b = np.zeros(20)
c = np.append(a[0:10],b[0:10])
df = pd.DataFrame({'a':a,'b':b,'c':c},
  index=pd.date_range('1/1/2000', periods=20))

# plot original data
plt.plot(a)
plt.plot(c)
plt.title('original data')
plt.show()

# plot rolling correlation
corrs = df.rolling(window=5,center=True).corr()
corrs.loc[:, 'a', 'c'].plot(title = 'rolling correlation')

