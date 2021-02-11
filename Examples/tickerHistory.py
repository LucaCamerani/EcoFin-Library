"""
tickerHistory.py

Created by Luca Camerani at 06/10/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import matplotlib.pyplot as plt

from EcoFin.dataDownload.ticker import Ticker

ticker = Ticker('MSFT')

history = ticker.getHistory().tail(100)

plt.plot(history.index, history.Close, label='Price ($S_t$)')
plt.show()

print(ticker.getInfo())
