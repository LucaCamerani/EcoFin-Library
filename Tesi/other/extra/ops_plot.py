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

fig, axs = plt.subplots(2, gridspec_kw={'height_ratios': [3, 2]}, figsize=(10, 5), sharex=True)

"""
# chart 1
axs[0].plot(data.strike, data['BSMPrice_call'], linewidth=3, label='Theoretical call', color='green')
axs[0].plot(data.strike, data['BSMPrice_put'], linewidth=3, label='Theoretical put', color='red')
axs[0].plot(data.strike, data.avgPrice_call, linewidth=3, linestyle="dashed", label='$Call_{AVG}$')
axs[0].plot(data.strike, data.avgPrice_put, linewidth=3, linestyle="dashed", label='$Put_{AVG}$')

axs[0].plot(forwardPrice, 0, markersize=8, marker="^", color='violet')
prices = data[['avgPrice_call', 'avgPrice_put']].to_numpy()
axs[0].vlines(forwardPrice, np.nanmin(prices), np.nanmax(prices),
           linestyles="dotted", color='violet', alpha=.6, label='Forward Price')
axs[0].legend(loc=2)
"""

# chart 1
lines = []
lines.append(axs[0].bar(data.strike, data['openInterest_call'],
                        label='Open Interest (Call)', color='green', alpha=.3))
lines.append(axs[0].bar(data.strike, data['openInterest_put'],
                        label='Open Interest (Put)', color='red', alpha=.3))

ax_ter = axs[0].twinx()
lines.append(ax_ter.plot(data.strike, data['weights'],
                         label='Weights', color='gold', linewidth=3)[0])
ax_ter.axes.get_yaxis().set_visible(False)
axs[0].legend(lines, [l.get_label() for l in lines], loc=0)

# chart 2
axs[1].plot(data.strike, data['spreadSummary'], linewidth=3, label=r'$\lambda^{OPS}$')
axs[1].plot(data.strike, data['spread_call'], label='$Spread_{CALL}$', color='green', alpha=.5)
axs[1].plot(data.strike, data['spread_put'], label='$Spread_{PUT}$', color='red', alpha=.5)
axs[1].hlines(0, np.min(data.strike), np.max(data.strike), linestyles="dotted", color='black', alpha=.6, label='cut-off')
axs[1].legend(loc=2)

plt.tight_layout()
plt.show()
