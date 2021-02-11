"""
benchmarkChart.py

Created by Luca Camerani at 06/02/2021, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tqdm import tqdm

# -------------------------[Set-up]-------------------------
ticker_list = [line.rstrip('\n') for line in open(r'../INDEXs/DJIA.txt')]
maturity_min = 15

base_path = r'../Export/BackTest_C'

start_date = 0
driver = 'SpotPrice'

# ----------------------------------------------------------
data = {driver: {}}
for tick in tqdm(ticker_list, desc='Importing data'):
    try:
        # Import data and clean-up
        source = pd.read_excel(r'{}/{}/backTest_[{}].xlsx'.format(base_path, tick, maturity_min), engine='openpyxl')
        source = source.loc[source['Date'] >= start_date, ~source.columns.str.contains('^Unnamed')]
        source.set_index(pd.to_datetime(source['Date'], format='%Y%m%d'), drop=True, inplace=True)

        data[driver][tick] = source[driver]
    except:
        pass

# Merge data
data[driver] = pd.concat(data[driver], axis=1)

# Compute ln-returns table
data['lnReturns'] = np.log(data[driver].shift(-1) / data[driver])

# Plot results
fig, axs = plt.subplots(2, figsize=(15, 8), sharex=True)
fig.suptitle('Benchmark', fontsize=16)

# Plot benchmark
axs[0].set_title('Underlying returns')
for tick in data[driver].keys():
    axs[0].plot(np.cumsum(data['lnReturns'][tick]), label=tick)
axs[0].set(ylabel=r'ln-returns ($X_t$)')
axs[0].legend(ncol=4)

# Plot strategy return vs. benchmark (portfolio)
axs[1].set_title('Portfolio return')
axs[1].plot(np.cumsum(data['lnReturns'].sum(axis=1)), label='Benchmark')
axs[1].set(xlabel=r'Time ($t$)', ylabel=r'ln-returns ($X_t$)')
axs[1].legend()

# Compute performance metrics
SR_b = data['lnReturns'].sum(axis=1).sum() / data['lnReturns'].sum(axis=1).std()

print('Sharpe-Ratio:\n • Benchmark: {}'.format(SR_b))

plt.show()
