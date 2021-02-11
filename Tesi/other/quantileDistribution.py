"""
quantileDistribution.py

Created by Luca Camerani at 04/02/2021, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import matplotlib.pyplot as plt
import pandas as pd
import scipy as sp
import seaborn as sns

# -------------------------[Set-up]-------------------------
ticker_list = [line.rstrip('\n') for line in open(r'../INDEXs/DJIA.txt')]
maturity_min = 15
base_path = r'../Export/BackTest'
start_date = 0
tick = 'MSFT'
driver = 'OPS_[OI]'
alpha = .1
# -------------------------[Set-up]-------------------------

# Import data and clean-up
data = pd.read_excel(r'{}/{}/backTest_[{}].xlsx'.format(base_path, tick, maturity_min), engine='openpyxl')
data = data.loc[data['Date'] >= start_date, ~data.columns.str.contains('^Unnamed')]
data.set_index(pd.to_datetime(data['Date'], format='%Y%m%d'), drop=True, inplace=True)

# Plot results
fig, axs = plt.subplots(1, 2, figsize=(15, 5), gridspec_kw={'width_ratios': [4, 1]}, sharey=True)
fig.suptitle('Quantile Correlation (QC)', fontsize=16)

# 1) Plot driver and quantiles
axs[0].set_title('Indicator')
axs[0].scatter(data.index, data[driver], alpha=.3, label='OPS')
axs[0].axhline(y=data[driver].quantile(1 - alpha), color='green', linestyle='--', label=r'$Q_{1-\alpha}$')
axs[0].axhline(y=data[driver].quantile(alpha), color='red', linestyle='--', label=r'$Q_{\alpha}$')
axs[0].legend()

# 2) Plot distribution
axs[1].set_title('Distribution')
axs[1].hist(data[driver], bins=40, density=True, orientation='horizontal')
axs[1] = sns.distplot(data[driver], fit=sp.stats.norm, kde=False, hist=False, vertical=True, label='Normal Fit')
axs[1].legend()

plt.subplots_adjust(wspace=0, hspace=0)
plt.show()
