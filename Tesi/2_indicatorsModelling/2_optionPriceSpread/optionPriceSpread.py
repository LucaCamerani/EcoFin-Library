"""
2_optionPriceSpread.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import os

import matplotlib.pyplot as plt
import numpy as np

from EcoFin.dataDownload.optionsManager import OptionManager
from EcoFin.dataDownload.ticker import Ticker
from EcoFin.options.deepOptionChain import DeepOptionChain
from EcoFin.stat.utils import weightedAvg, weightedStd

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

data['weights'] = data.loc[:, ['openInterest_call', 'openInterest_put']].sum(axis=1) / \
                  np.nansum(data.loc[:, ['openInterest_call', 'openInterest_put']].to_numpy())

fig, axs = plt.subplots(3, figsize=(15, 8), sharex=True)
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
axs[1].set_title('Option Price Spread ($OPS$)')
axs[1].plot(data.strike, data['spread_call'], label='$Spread_{CALL}$', color='green', alpha=.5)
axs[1].plot(data.strike, data['spread_put'], label='$Spread_{PUT}$', color='red', alpha=.5)
axs[1].plot(data.strike, data['spreadSummary'], label='$Spread_{SUMMARY}$', linewidth=3, linestyle="dotted")
spreads = data[['spread_call', 'spread_put']].to_numpy()
axs[1].vlines(forwardPrice, np.nanmin(spreads), np.nanmax(spreads),
              linestyles="dashed", color='violet', alpha=.6, label='Forward Price')
axs[1].legend()
axs[1].grid()

# chart 3
lines = []
axs[2].set_title('Weights')
lines.append(axs[2].plot(data.strike, np.abs(data.moneyness), label='$Moneyness$')[0])
lines.append(axs[2].vlines(forwardPrice, 0, np.nanmax(data.moneyness),
                           linestyles="dashed", color='violet', alpha=.6, label='Forward Price'))
axs[2].set(xlabel='Strike')
axs[2].grid()

ax_bis = axs[2]
lines.append(ax_bis.bar(data.strike, data['openInterest_call'],
                        label='Open Interest (Call)', color='green', alpha=.3))
lines.append(ax_bis.bar(data.strike, data['openInterest_put'],
                        label='Open Interest (Put)', color='red', alpha=.3))

ax_ter = axs[2].twinx()
lines.append(ax_ter.plot(data.strike, data['weights'],
                         label='Weights', color='blue', alpha=.3)[0])

axs[2].legend(lines, [l.get_label() for l in lines], loc=0)

plt.figtext(.9, 0.02, "{} | {}".format(optionChain.getChainDate(), optionChain.getChainExpiration()),
            ha="right", fontsize=10, bbox={"facecolor": "orange", "alpha": 0.2, "pad": 8})
plt.show()

summary = {'Mean': weightedAvg(data['spreadSummary'], data['weights']),
           'Std': weightedStd(data['spreadSummary'], data['weights'])}
print('Summary: {}'.format(summary))

# ----------------------[EXPORT BLOCK]--------------------------------
path = '../Export/[{}]_({})'.format(ticker.ticker, ticker_info.longName)
if not os.path.exists(path):
    os.makedirs(path)

fig.savefig('{}/optionPriceSpread_[{}].png'.format(path, exp))
# ----------------------[EXPORT BLOCK]--------------------------------
