"""
3_strategyTester.py

Created by Luca Camerani at 03/02/2021, University of Milano-Bicocca.
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

# -------------------------[Set-up]-------------------------
ticker_list = [line.rstrip('\n') for line in open(r'../INDEXs/DJIA.txt')]
maturity_min = 15

base_path = r'../Export/BackTest_C'
start_date = 0

direction = 'OPS_[OI]'
force = 'VIX_[CBOE]'  # In None, don't use force driver
polarize = True
buy_only = False
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
# ⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕[SET-UP]⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕
limit = 0 if buy_only else -1
if polarize:
    data[direction] = utils.polarizeTable(data[direction], under=limit)

if force is None:
    data[force] = 1

data['signals'] = data[direction] * data[force]
# ⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕[SET-UP]⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕⭕

# Set compensation leverage
l = data['signals'].abs().mean(axis=1).mean() ** (-1)

# Compute ln-returns table
data['lnReturns'] = np.log(data['SpotPrice'].shift(-1) / data['SpotPrice'])
data['strategy'] = data['lnReturns'] * data['signals'] * l

# Plot results
fig, axs = plt.subplots(3, figsize=(15, 8), sharex=True)
fig.suptitle('Strategy tester', fontsize=16)

# Plot signals
axs[0].set_title('Benchmark returns')
axs[1].set_title('Signals')
for tick in data['strategy'].keys():
    axs[0].plot(np.cumsum(data['lnReturns'][tick]), label=tick)
    axs[1].scatter(data['strategy'][tick].index,
                   data['strategy'][tick], alpha=.3, label=tick)

axs[0].set(ylabel=r'ln-returns ($X_t$)')
axs[0].legend(ncol=4)

# Plot strategy return vs. benchmark (portfolio)
axs[2].set_title('Portfolio returns')
axs[2].plot(np.cumsum(data['lnReturns'].sum(axis=1)), label='Benchmark')
axs[2].plot(np.cumsum(data['strategy'].sum(axis=1)), label='Strategy')
axs[2].set(xlabel=r'Time ($t$)', ylabel=r'ln-returns ($X_t$)')
axs[2].legend()

# Compute performance metrics
SR_b = data['lnReturns'].mean(axis=1).sum() / data['lnReturns'].mean(axis=1).std()
SR_s = data['strategy'].mean(axis=1).sum() / data['strategy'].mean(axis=1).std()

performance = Performance(data['lnReturns'].mean(axis=1), data['strategy'].mean(axis=1))
performance.printPerformanceSummary()

plt.show()
