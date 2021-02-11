"""
!_optionPriceSurface.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import matplotlib.pyplot as plt
import numpy as np

from EcoFin.dataDownload.ticker import Ticker

# [1] Setup variables
ticker = Ticker('MSFT')

# [2] Get data regarding optionsExp and merge in a variable
surfaces = getPricesSurface(ticker)

# [3] Prepare plot area
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
fig.suptitle('Option price surfaces')

# [4] Plot surfaces for Call and Put optionsExp
for type in ['call', 'put']:
    if type == 'call':
        surface = surfaces.call
    else:
        surface = surfaces.put

    maturity = surface['maturity']

    X, Y = np.meshgrid(surface['strike'], maturity)
    Z = np.array(surface['prices'])

    surf = ax.plot_surface(X, Y, Z, alpha=0.6, label='{} price'.format(type))
    surf._facecolors2d = surf._facecolors3d
    surf._edgecolors2d = surf._edgecolors3d

ax.set_xlabel('Strike')
ax.set_ylabel('Days to maturity')
ax.set_zlabel('Price')
ax.legend()

plt.show()
