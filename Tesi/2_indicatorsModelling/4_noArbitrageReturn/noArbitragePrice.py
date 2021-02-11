"""
4_noArbitragePrice.py

Created by Luca Camerani at 22/11/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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

data['weights'] = data.loc[:, ['openInterest_call', 'openInterest_put']].sum(axis=1) / \
                  np.nansum(data.loc[:, ['openInterest_call', 'openInterest_put']].to_numpy())

history_back = 100
history = ticker.getHistory(end=optionChain.getChainDate()).tail(history_back)

data['S_mean'] = np.mean(data[['S_U', 'S_L']], axis=1)
forecast = np.mean(data[['S_U', 'S_L', 'S_mean']])

fig, axs = plt.subplots(3, figsize=(15, 8))
fig.suptitle('No-arbitrage price bounds ({})'.format(ticker_info.longName), fontsize=16)

# chart 1
axs[0].set_title('No arbitrage price bounds')
axs[0].plot(data.strike, data['S_U'], label='Upper bound ($S^{U})_{now}$)', color='green')
axs[0].plot(data.strike, data['S_L'], label='Lower bound ($S^{L})_{now}$)', color='red')

axs[0].plot(data.strike, data['S_mean'], label='Price AVG ($S{AVG})_{now}$)', linewidth=3, linestyle="dotted")
bounds = data[['S_U', 'S_L']]
axs[0].plot(forwardPrice, np.nanmin(bounds), markersize=8, marker='^', color='violet')
axs[0].vlines(forwardPrice, np.nanmin(bounds), np.nanmax(bounds),
              linestyles='dashed', color='violet', alpha=.6, label='Forward Price')
axs[0].legend()
axs[0].grid()

# chart 2
axs[1].set_title('Market underlying price forecast')
axs[1].plot(history.index, history.Close, label='Underlying price ($S_t$)')

funnel = pd.DataFrame({'S_U': [history.tail(1).Close.values[0], forecast['S_U']],
                       'S_mean': [history.tail(1).Close.values[0], forecast['S_mean']],
                       'S_L': [history.tail(1).Close.values[0], forecast['S_L']]},
                      index=[history.tail(1).index.values[0], np.datetime64(datetime.utcfromtimestamp(exp))])

axs[1].plot(funnel.index, funnel['S_U'], color='green', linestyle="dotted", label='$S^{U}$')
axs[1].plot(funnel.index, funnel['S_mean'], color='blue', label='$S^{AVG}$')
axs[1].plot(funnel.index, funnel['S_L'], color='red', linestyle="dotted", label='$S^{L}$')
axs[1].plot(datetime.utcfromtimestamp(exp), forecast['S_mean'], '<')

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

print('Price: {}'.format(forecast['S_mean']))

# ----------------------[EXPORT BLOCK]--------------------------------
path = '../Export/[{}]_({})'.format(ticker.ticker, ticker_info.longName)
if not os.path.exists(path):
    os.makedirs(path)

fig.savefig('{}/noArbitrageBounds_[{}].png'.format(path, exp))
# ----------------------[EXPORT BLOCK]--------------------------------
