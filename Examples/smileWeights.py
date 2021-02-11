"""
smileWeights.py

Created by Luca Camerani at 04/01/2021, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import matplotlib.pyplot as plt
import numpy as np

from EcoFin.dataDownload.optionsManager import OptionManager
from EcoFin.dataDownload.ticker import Ticker
from EcoFin.options.chainWeights import ChainWeights
from EcoFin.options.impliedVolatility import ImpliedVolatility
from EcoFin.options.volatilitySmile import VolatilitySmile

# -------------------------[Set-up]-------------------------
ticker = Ticker('MSFT')
optionManager = OptionManager(ticker, now=None)

i = 0  # <- Time To Maturity curve
exp = optionManager.getExpirations()[i]

optionChain = optionManager.getOptionChain(exp=exp)
# ----------------------------------------------------------

fig, axs = plt.subplots(2, figsize=(15, 8), sharex=True)
fig.suptitle('Weigh implied volatility ({})'.format(ticker.getInfo().ticker), fontsize=16)

forwardPrice = optionChain.getForwardPrice()
impliedVolatility = ImpliedVolatility(optionChain)
volatilitySmile = VolatilitySmile(impliedVolatility)
smile = volatilitySmile.getVolatilitySmile()

chainWeights = ChainWeights(optionChain)
weights = chainWeights.computeMoneynessWeights()

# chart 1
axs[0].set_title('Volatility smile (VS)')
axs[0].plot(smile.strike, smile.smile, label='Smile')

axs[0].plot(forwardPrice, np.amin(smile.smile) * 0.7, markersize=8, marker="^", color='violet')
axs[0].vlines(forwardPrice, np.nanmin(smile.smile) * 0.7, np.nanmax(smile.smile),
              linestyle="dashed", color='violet', alpha=.6, label='Forward Price')
axs[0].set(ylabel='Volatility',
           title='Option volatility smile')
axs[0].legend()
axs[0].grid()

# chart 2
axs[1].set_title('Weights')
axs[1].plot(weights, label='Weights ($w$)', color='green', alpha=.5, linewidth=4)
axs[1].vlines(forwardPrice, np.nanmin(weights) * 0.7, np.nanmax(weights) * 1.5,
              linestyle="dashed", color='violet', alpha=.6, label='Forward Price')
axs[1].set(xlabel='Strike', ylabel='Weights')
axs[1].legend()
axs[1].grid()

plt.show()
