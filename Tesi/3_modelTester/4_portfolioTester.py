"""
4_portfolioTester.py

Created by Luca Camerani at 10/02/2021, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm

from EcoFin.assetAllocation.performance import Performance
from EcoFin.utils import utils
from EcoFin.assetAllocation.allocation import Allocation


# -------------------------[Set-up]-------------------------
ticker_list = [line.rstrip('\n') for line in open(r'../INDEXs/DJIA.txt')]
maturity_min = 15

base_path = r'../Export/BackTest_C'
start_date = 0

# Strategy set-up
direction = 'OPS_[OI]'      # Direction driver
force = 'VIX_[CBOE]'        # In None, don't use force driver
polarize = True             # True or False: polarize direction component

# Portfolio set-up
buy_only = True             # Set a buy only strategy that ignore negative signals
w_limit = 5                 # Ranks best N ticker based on strategy
w_equally = True            # Equally weighted mode
leverage = None             # Strategy leverage (1 is no leverage, None is auto-compensation)
# ----------------------------------------------------------

base = ['SpotPrice']
data = {b: {} for b in base + [direction, force]}
if None in data.keys():
    del data[None]

for tick in tqdm(ticker_list, desc='Importing data'):
    try:
        # Import data and clean-up
        source = pd.read_excel(r'{}/{}/backTest_[{}].xlsx'.format(base_path, tick, maturity_min), engine='openpyxl')
        source = source.loc[source['Date'] >= start_date, ~source.columns.str.contains('^Unnamed')]
        source.set_index(pd.to_datetime(source['Date'], format='%Y%m%d'), drop=True, inplace=True)

        for driver in data.keys():
            data[driver][tick] = source[driver]
    except:
        pass

# Merge (concatenate) data and create dataframes
for driver in data.keys():
    data[driver] = pd.concat(data[driver], axis=1)

    # ❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌[Normalize direction data]❌❌❌❌❌❌❌❌❌❌❌
    if driver == direction:
        data[driver] = data[driver].sub(data[driver].mean(axis=1), axis=0)
    # ❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌

# Generate strategy signals
# -----------------------------------[STRATEGY SET-UP]-----------------------------------
if polarize:                                                                            #
    data[direction] = utils.polarizeTable(data[direction])                              #
                                                                                        #
if force is None:                                                                       #
    force_v = 1                                                                         #
else:                                                                                   #
    force_v = data[force]                                                               #
                                                                                        #
data['signals'] = data[direction] * force_v                                             #
# -----------------------------------[STRATEGY SET-UP]-----------------------------------

# =====================================================================================
#                       FROM HERE NO 'signals data' MANIPULATION
# =====================================================================================

# [1] Compute ln-returns of benchmark
data['lnReturns'] = np.log(data['SpotPrice'].shift(-1) / data['SpotPrice'])

# [2] Compute strategy weights
allocation = Allocation(data['signals'], buyOnly=buy_only, limit=w_limit)
if w_equally:
    data['weights'] = allocation.getEquallyWeights()
else:
    data['weights'] = allocation.getSignalWeights()

# [3] Compute strategy ln-returns
if leverage is None: leverage = data['SpotPrice'].shape[1]
data['strategy'] = data['lnReturns'] * data['weights'] * leverage

# Compute performance metrics
performance = Performance(data['lnReturns'].mean(axis=1), data['strategy'].mean(axis=1), r=0.019)
performance.printPerformanceSummary()

# =====================================================================================
#                       FROM HERE NO DATA MANIPULATION
# =====================================================================================

# Create plot framework
fig, axs = plt.subplots(2, figsize=(15, 8), sharex=True)
fig.suptitle('Strategy tester', fontsize=16)

# Plot strategy return vs. benchmark (data)
axs[0].set_title('data returns')
axs[0].plot(data['lnReturns'].mean(axis=1).cumsum(), label='Benchmark')
axs[0].plot(data['strategy'].mean(axis=1).cumsum(), label='Strategy')
axs[0].set(ylabel='Cumulated ln-returns ($X_t$)')
axs[0].legend()

# Plot number of assets in portfolio
ax2 = axs[0].twinx()
color = 'tab:gray'
ax2.set_ylabel('Number of assets', color=color)
ax2.plot(allocation.countAssets(data['weights']), linewidth=.5, color=color)
ax2.tick_params(axis='y', labelcolor=color)

# Plot evolution of weights
positive = data['weights'][data['weights'] >= 0].fillna(0)
negative = data['weights'][data['weights'] < 0].fillna(0)

axs[1].set_title('Weights evolution')
axs[1].stackplot(data['weights'].index, positive.T)
axs[1].stackplot(data['weights'].index, negative.T)
axs[1].plot(allocation.getBalancing(data['weights']), linewidth=1, linestyle="dotted",
            color='black', alpha=.6, label='Balancing ($\mu$)')
axs[1].set(xlabel=r'days ($t$)', ylabel=r'data weights')
axs[1].legend()

with pd.ExcelWriter('{}/portfolio.xlsx'.format(base_path)) as writer:
    data['SpotPrice'].to_excel(writer, sheet_name='SpotPrices', index=True)
    data['lnReturns'].to_excel(writer, sheet_name='lnReturns', index=True)
    data['signals'].to_excel(writer, sheet_name='Signals', index=True)
    data['weights'].to_excel(writer, sheet_name='Weights', index=True)
    data['strategy'].to_excel(writer, sheet_name='Strategy', index=True)

plt.show()
