"""
6_putCallDelta.py

Created by Luca Camerani at 29/12/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import matplotlib.pyplot as plt
import numpy as np

from EcoFin.dataDownload.optionsManager import OptionManager
from EcoFin.dataDownload.ticker import Ticker
from EcoFin.options.deepOptionChain import DeepOptionChain

# -------------------------[Set-up]-------------------------
ticker = Ticker('MSFT')
optionManager = OptionManager(ticker, now=1492646400)
exp = optionManager.getExpirationByMaturity(30, method='greater')
optionChain = optionManager.getOptionChain(exp=exp)
# ----------------------------------------------------------

ticker_info = ticker.getInfo()
forwardPrice = optionChain.getForwardPrice()

deepOptionChain = DeepOptionChain(optionChain)
data = deepOptionChain.getDeepOptionChain()

fig, axs = plt.subplots(2, figsize=(15, 8), sharex=True)
fig.suptitle('Option prices spread analysis ({})'.format(ticker_info.longName), fontsize=16)

# chart 1
axs[0].set_title('Option market price curve vs. theorichal prices')
axs[0].plot(data.strike, data['TheoPrice_call'], linestyle="dotted", label='Theoretical call')
axs[0].plot(data.strike, data['TheoPrice_put'], linestyle="dotted", label='Theoretical put')
axs[0].plot(data.strike, data.avgPrice_call, label='$Call_{AVG}$', color='green')
axs[0].plot(data.strike, data.avgPrice_put, label='$Put_{AVG}$', color='red')

axs[0].plot(forwardPrice, 0, markersize=8, marker="^", color='violet')
prices = data[['avgPrice_call', 'avgPrice_put']].to_numpy()
axs[0].vlines(forwardPrice, np.nanmin(prices), np.nanmax(prices),
              linestyles="dashed", color='violet', alpha=.6, label='Forward Price')
axs[0].legend()
axs[0].grid()

# chart 2
axs[1].set_title('Put-Call Price Delta')
axs[1].plot(data.strike, data['PutCallDelta'], label=r'$\Delta_{P-C}$')

axs[1].plot(forwardPrice, 0, markersize=8, marker="^", color='violet')
prices = data[['avgPrice_call', 'avgPrice_put']].to_numpy()
axs[1].vlines(forwardPrice, np.nanmin(prices), np.nanmax(prices),
              linestyles="dashed", color='violet', alpha=.6, label='Forward Price')

price = data.loc[data['PutCallDelta'].idxmin(), 'strike']
axs[1].vlines(price, np.nanmin(prices), np.nanmax(prices),
              linestyles="dotted", color='blue', alpha=.8, label='$min(\Delta_{P-C})$')

axs[1].legend()
axs[1].grid()

plt.figtext(.9, 0.02, "{} | {}".format(optionChain.getChainDate(), optionChain.getChainExpiration()),
            ha="right", fontsize=10, bbox={"facecolor": "orange", "alpha": 0.2, "pad": 8})
plt.show()
