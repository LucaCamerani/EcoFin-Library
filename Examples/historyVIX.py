"""
historyVIX.py

Created by Luca Camerani at 05/01/2021, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import os

import matplotlib.pyplot as plt
from tqdm import tqdm

from EcoFin.dataDownload.optionsManager import OptionManager
from EcoFin.dataDownload.ticker import Ticker
from EcoFin.options.deepOptionChain import DeepOptionChain
from EcoFin.options.equityVIX import EquityVIX
from EcoFin.utils.utils import *

# -------------------------[Set-up]-------------------------
ticker = Ticker('MSFT')
optionManager = OptionManager(ticker)

# Custom
increment = 86400  # 1 day
date1 = 1483228800  # Sunday 01 January 2017
date2 = date1 + increment * 365 * 3
# ----------------------------------------------------------

ticker_info = ticker.getInfo()

output = []
for now in tqdm(range(date1, date2, increment), desc='Compute history'):  # Compute day by day
    if optionManager.setNow(now) is not False:
        exp = optionManager.getExpirationByMaturity(5, method='greater')
        optionChain = optionManager.getOptionChain(exp=exp)
        deepOptionChain = DeepOptionChain(optionChain, computeIV=True, progressBar=False)

        VIX = EquityVIX(deepOptionChain)

        summary = {'Date': unixtimestamp_to_date(optionChain.getChainDate()),
                   'SpotPrice': optionChain.getSpotPrice(),
                   'CBOE_VIX': VIX.getCBOEVIX(),
                   'Mean': VIX.getMeanVIX().value,
                   'Beta': VIX.getBetaVIX().value,
                   'ATM': VIX.getATMVIX().value,
                   'OI': VIX.getOpenInterestVIX().value
                   }

        if len(output) == 0:
            output = pd.DataFrame(columns=list(summary.keys()), index=[])

        output = output.append(summary, ignore_index=True)

fig, axs = plt.subplots(3, figsize=(15, 8), sharex=True, gridspec_kw={'height_ratios': [3, 3, 5]})
fig.suptitle('Option Volatility Smile analysis ({})'.format(ticker_info.ticker), fontsize=16)

# chart 1
axs[0].set_title('Underlying price')
axs[0].plot(output['SpotPrice'], label='Spot price ($S_t$)')
axs[0].set(ylabel='Price')
axs[0].legend()
axs[0].grid()

# chart 2
axs[1].set_title('CBOE VIX')
axs[1].plot(output['CBOE_VIX'], color='c', label='EVI$')
axs[1].set(ylabel='%')
axs[1].legend()
axs[1].grid()

# chart 3
axs[2].set_title('Volatility smile synthesis')

axs[2].plot(output['Mean'], label='Equally weighted')
axs[2].plot(output['Beta'], label='$BetaBin$')
axs[2].plot(output['ATM'], label='$Dirac$')
axs[2].plot(output['OI'], label='Open Interest')

axs[2].set(xlabel='Time ($t$)', ylabel=r'$\sigma_IV$')
axs[2].legend()
axs[2].grid()

plt.show()

# ----------------------[EXPORT BLOCK]--------------------------------
path = '../Export/[{}]'.format(ticker.ticker)
if not os.path.exists(path):
    os.makedirs(path)
with pd.ExcelWriter('{}/historyVIX_[{}].xlsx'.format(path, exp)) as writer:
    output.to_excel(writer, sheet_name='Chain', index=False)

print('\nFile saved!')
# ----------------------[EXPORT BLOCK]--------------------------------
