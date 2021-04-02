"""
2_optionPriceSpread.py

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
from EcoFin.options.blackScholesModel import BSM
from EcoFin.stat.equityVolatility import EquityVolatility

# -------------------------[Set-up]-------------------------
ticker = Ticker('MSFT')
optionManager = OptionManager(ticker, now=None)

i = 0  # <- Time To Maturity curve
exp = optionManager.getExpirations()[i]

optionChain = optionManager.getOptionChain(exp=exp)
# ----------------------------------------------------------

strikeList = optionChain.getStrikeList()

volatility_back = 260
series = ticker.getHistory(end=optionChain.getChainDate()).tail(volatility_back)
price = optionChain.getSpotPrice()

r = optionChain.getRiskFreeRate()
sigma = EquityVolatility(series).meanSigma()
maturity = optionChain.getTimeToMaturity().days

forwardPrice = optionChain.getForwardPrice()

fig, ax = plt.subplots()

chain = optionChain.getChain()
theoreticalPrices = {'call': [], 'put': []}

for strike in strikeList:
    option = BSM(price, strike, r, sigma, maturity)
    optPrice = option.computePrice()

    theoreticalPrices['call'].append(optPrice.call)
    theoreticalPrices['put'].append(optPrice.put)

ax.plot(strikeList, theoreticalPrices['call'], linestyle="dotted", label='Theoretical call')
ax.plot(strikeList, theoreticalPrices['put'], linestyle="dotted", label='Theoretical put')

ax.plot(chain.calls.strike, chain.calls.avgPrice, label='$Call_{AVG}$')
ax.plot(chain.puts.strike, chain.puts.avgPrice, label='$Put_{AVG}$')

ax.plot(forwardPrice, 0, markersize=8, marker="^", color='violet')
ax.vlines(forwardPrice, 0, np.amax(chain.calls.avgPrice + chain.puts.avgPrice),
          linestyles="dashed", color='violet', alpha=.6, label='Forward Price')

ax.set(xlabel='Strike', ylabel='Price',
       title='Option price curve comparison')
ax.legend()

plt.grid()
plt.show()
