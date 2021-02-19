"""
5_costsTester.py

Created by Luca Camerani at 18/02/2021, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

"""
4_portfolioTester.py

Created by Luca Camerani at 10/02/2021, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import math
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
buy_only = False            # Set a buy only strategy that ignore negative signals
w_limit = None              # Ranks best N ticker based on strategy
w_equally = False           # Equally weighted mode
leverage = None             # Strategy leverage (1 is no leverage, None is auto-compensation)

# Transaction costs
tc = 8                      # unit in basis points
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
if leverage is None:
    leverage = data['SpotPrice'].shape[1]
data['strategy'] = data['lnReturns'] * data['weights'] * leverage

# Compute turnover and transaction costs
turnover = allocation.getTurnover(data['weights'])
data['costs'] = np.log(turnover.byTime * 2 * (tc/1e4) + 1)
data['strategy_net'] = data['strategy'].mean(axis=1) - data['costs']

# =====================================================================================
#                       FROM HERE NO DATA MANIPULATION
# =====================================================================================

# Create plot framework
fig, axs = plt.subplots(2, figsize=(15, 8), sharex=True)
fig.suptitle('Strategy tester', fontsize=16)

# Plot strategy return vs. benchmark (data)
axs[0].set_title('data returns')
axs[0].plot(data['lnReturns'].mean(axis=1).cumsum(), linestyle='dotted', label='Benchmark')
axs[0].plot(data['strategy'].mean(axis=1).cumsum(), label='Strategy Gross')
axs[0].plot(data['strategy_net'].cumsum(), label='Strategy Net')
axs[0].set(ylabel='Cumulated ln-returns ($X_t$)')
axs[0].legend()

# Plot number of assets in portfolio
ax2 = axs[0].twinx()
color = 'tab:gray'
ax2.set_ylabel('Transaction Costs', color=color)
ax2.fill_between(data['costs'].index, 0, data['costs'], linewidth=.5, alpha=.2, color=color)
ax2.plot(data['costs'], linewidth=.5, alpha=.6, color=color)
ax2.set_ylim([0, data['costs'].max() * 4])
ax2.tick_params(axis='y', labelcolor=color)

# Plot evolution of weights
axs[1].set_title('Transition costs')
axs[1].plot(turnover.byTime, color='gold', label=r'Turnover ($\gamma$)')
axs[1].axhline(turnover.mean, alpha=.6, linestyle='--', label=r'mean')
axs[1].legend()

plt.show()
