"""
!_optionPriceCurve.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import time

import matplotlib.pyplot as plt

from EcoFin.dataDownload.ticker import Ticker
from EcoFin.options.optionChain import OptionChain

ticker = Ticker('MSFT')

i = 0
while time.time() >= ticker.optionsExp[i]:
    i += 1
exp = ticker.optionsExp[i]

optionChain = OptionChain(ticker, expiration=exp)
data = getPricesCurve(optionChain)

fig, ax = plt.subplots()

for type in ['call', 'put']:
    if type == 'call':
        ax.plot(data.call['strike'], data.call['prices'], label=type)
    else:
        ax.plot(data.put['strike'], data.put['prices'], label=type)

ax.set(xlabel='Strike', ylabel='Price',
       title='Option price curve')
ax.legend()
ax.grid()

plt.show()
