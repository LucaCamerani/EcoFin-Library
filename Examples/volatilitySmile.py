"""
volatilitySmile.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import matplotlib.pyplot as plt
import numpy as np

from EcoFin.dataDownload.optionsManager import OptionManager
from EcoFin.dataDownload.ticker import Ticker
from EcoFin.options.impliedVolatility import ImpliedVolatility
from EcoFin.options.volatilitySmile import VolatilitySmile

# -------------------------[Set-up]-------------------------
ticker = Ticker('MSFT')
optionManager = OptionManager(ticker, now=None)

i = 0  # <- Time To Maturity curve
exp = optionManager.getExpirations()[i]

optionChain = optionManager.getOptionChain(exp=exp)
# ----------------------------------------------------------

price = optionChain.getSpotPrice()
forwardPrice = optionChain.getForwardPrice()

impliedVolatility = ImpliedVolatility(optionChain)
volatilitySmile = VolatilitySmile(impliedVolatility)
smile = volatilitySmile.getVolatilitySmile()

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(smile.strike, smile.smile, label='Smile', alpha=.5)
ax.plot(smile.strike, smile.naturalSmile, linestyle='dotted', label='Original Smile')

ax.plot(forwardPrice, np.amin(smile.smile) * 0.5, markersize=8, marker="^", color='violet')
ax.vlines(forwardPrice, np.amin(smile.smile) * 0.5, np.amax(smile.smile),
          linestyles="dashed", color='violet', alpha=.6, label='Forward Price')

ax.set(xlabel='Strike', ylabel='Volatility',
       title='Option volatility smile ({})'.format(ticker.getInfo().ticker))
ax.legend()
ax.grid()

plt.show()
