"""
volatilitySurface.py

Created by Luca Camerani at 11/12/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import cm

from EcoFin.dataDownload.optionsManager import OptionManager
from EcoFin.dataDownload.ticker import Ticker
from EcoFin.options.deepOptionSurface import DeepOptionSurface
from EcoFin.options.utils import daysToMaturity

ticker = Ticker('MSFT')
optionManager = OptionManager(ticker, now=1551657600)

optSurface = optionManager.getOptionSurface()
deepSurface = DeepOptionSurface(optSurface, computeIV=True)

# get IV surface data
exps = optSurface.getExpirations()

extraction = ['strike', 'smile']
surfaceData = deepSurface.getDeepChainByDate(exps[0]).getDeepOptionChain()[extraction]. \
    rename(columns={'smile': 'smile_{}'.format(exps[0])})

for exp in exps[1:]:
    currentDeepChain = deepSurface.getDeepChainByDate(exp).getDeepOptionChain()

    surfaceData = pd.merge(surfaceData, currentDeepChain[extraction],
                           on='strike', suffixes=['', '_{}'.format(exp)])

surfaceData.set_index('strike', inplace=True)

x = daysToMaturity(exps, optSurface.getDate())
y = surfaceData.index
X, Y = np.meshgrid(x, y)
Z = surfaceData

fig = plt.figure(figsize=(10, 5))
fig.suptitle('Implied volatility surface (VS)', fontsize=16)

ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap=cm.coolwarm)

ax.set_xlabel(r'Days to maturity ($\tau$)')
ax.set_ylabel('Strike ($K$)')
ax.set_zlabel(r'IV ($\sigma^{IV}$)')

plt.show()
