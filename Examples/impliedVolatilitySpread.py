"""
3_impliedVolatilitySpread.py

Created by Luca Camerani at 18/10/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import matplotlib.pyplot as plt
import numpy as np

from EcoFin.dataDownload.optionsManager import OptionManager
from EcoFin.dataDownload.ticker import Ticker
from EcoFin.options.equityVIX import EquityVIX
from EcoFin.options.impliedVolatility import ImpliedVolatility
from EcoFin.options.volatilitySmile import VolatilitySmile

# -------------------------[Set-up]-------------------------
ticker = Ticker('MSFT')
optionManager = OptionManager(ticker, now=None)

i = 0  # <- Time To Maturity curve
exp = optionManager.getExpirations()[i]

optionChain = optionManager.getOptionChain(exp=exp)
# ----------------------------------------------------------

impliedVolatility = ImpliedVolatility(optionChain)
volatilitySmile = VolatilitySmile(impliedVolatility)
smile = volatilitySmile.getVolatilitySmile()

VIX = EquityVIX(volatilitySmile)
price = optionChain.getSpotPrice()
forwardPrice = optionChain.getForwardPrice()
spotPrice = optionChain.getSpotPrice()
sigma = VIX.getHistoricalVolatility()

fig, ax = plt.subplots(2)
ax[0].plot(smile.strike, smile.smile, label='Smile')
ax[0].plot(forwardPrice, np.amin(smile.smile), markersize=8, marker="^", color='violet')
ax[0].axhline(sigma, color='red', alpha=.6, linestyle='--', label=r'$\sigma$')
ax[0].axvline(forwardPrice, ymin=np.amin(smile.smile), ymax=np.amax(smile.smile),
              color='violet', alpha=.6, label='Forward Price')

ax[1].plot(smile.strike, sigma - smile.smile, label='Volatility Excess')
"""
ax[1].plot(smile.strike, np.abs(smile.moneyness-1), label=r'Moneyness $\frac{K}{S}$')
bounds = [np.amax(smile.moneyness-1), -np.amin(smile.moneyness-1)]
ax[1].axhline(np.amin(bounds), color='violet', alpha=.6, label='limit')
ax[1].legend()
"""

plt.show()
