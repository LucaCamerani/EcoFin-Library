"""
impliedProbability.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

from EcoFin.dataDownload.optionsManager import OptionManager
from EcoFin.dataDownload.ticker import Ticker
from EcoFin.options.impliedVolatility import ImpliedVolatility
from EcoFin.options.volatilitySmile import VolatilitySmile
from EcoFin.stat.empiricalDist import cdfTopdf, getClassSize

# -------------------------[Set-up]-------------------------
ticker = Ticker('MSFT')
optionManager = OptionManager(ticker, now=None)

i = 0  # <- Time To Maturity curve
exp = optionManager.getExpirations()[i]

optionChain = optionManager.getOptionChain(exp=exp)
# ----------------------------------------------------------

# [1] Compute volatility skew
impliedVolatility = ImpliedVolatility(optionChain)
volatilitySmile = VolatilitySmile(impliedVolatility)
smile = volatilitySmile.getVolatilitySmile()

# [2] Compute probabilities using BSM
cum = norm.cdf(smile.d2)
probs = cdfTopdf(1 - cum)

# [3] Plot results
fig, ax1 = plt.subplots(figsize=(10, 5))

color = 'tab:red'
ax1.set_xlabel('Strike')
ax1.set_ylabel('Cum. probabilities', color=color)
ax1.plot(smile.strike, cum, color=color)
ax1.tick_params(axis='y')

color = 'tab:blue'
ax2 = ax1.twinx()
ax2.set_ylabel('Probability', color=color)
ax2.bar(smile.strike, probs, getClassSize(smile.strike), color=color, alpha=0.6)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()

plt.plot(smile.strike, np.full(len(smile.strike), 0), markersize=5, marker="^", color='black')

plt.grid()
plt.show()
