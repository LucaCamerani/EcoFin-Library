"""
markowitzAllocation.py

Created by Luca Camerani at 13/09/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from EcoFin.assetAllocation.markowitzModel import MarkowitzModel
from EcoFin.dataDownload.ticker import Ticker

market = ['AAPL', 'AMZN', 'CSCO', 'MSFT', 'GOOGL']
marketDataFrame = pd.DataFrame(columns=market)

for company in market:
    ticker = Ticker(company)
    df = ticker.getHistory().tail(260)
    marketDataFrame[company] = df['Close']

model = MarkowitzModel(marketDataFrame)

randW = model.randomWeights(10000)

rets = []
stds = []
for r in randW:
    performance = model.portfolioPerformance(r)
    rets.append(performance.ret)
    stds.append(performance.std)

plt.scatter(stds, rets, alpha=.4, linewidths=.1, marker=".", label='Random portfolios')

effWeights = model.computeEfficientFrontier(returnSpace=np.arange(0, 1, .01))

effRets = []
effStds = []
sharpe = []
for w in effWeights:
    performance = model.portfolioPerformance(w)
    effRets.append(performance.ret)
    effStds.append(performance.std)
    sharpe.append(performance.SR)

plt.plot(effStds, effRets, color='red', linewidth=2, label='Efficient frontier')
plt.ylabel("Return")
plt.legend()

plt.twinx()
plt.plot(effStds, sharpe, color='orange', linewidth=1, label='Sharpe Ratio')
plt.ylabel("Sharpe Ratio")
plt.legend()

plt.xlabel("Volatility")
plt.show()
