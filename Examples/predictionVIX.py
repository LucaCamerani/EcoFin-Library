"""
predictionVIX.py

Created by Luca Camerani at 07/01/2021, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

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
date2 = date1 + increment * 900
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

fig, axs = plt.subplots(2, figsize=(15, 8), sharex=True, gridspec_kw={'height_ratios': [3, 5]})
fig.suptitle('Option Volatility Smile analysis ({})'.format(ticker_info.ticker), fontsize=16)


output['lnRet'] = np.abs(np.log(output['SpotPrice'].shift(-1) / output['SpotPrice']))

# chart 1
axs[0].set_title('Absolute returns')
axs[0].scatter(output['lnRet'].index, output['lnRet'], label='log-return ($X^f_t$)')
axs[0].set(ylabel='ln')
axs[0].legend()
axs[0].grid()

# chart 2
axs[1].set_title('Volatility metrics')
axs[1].plot(output['CBOE_VIX'], color='c', label='$EVI$')
axs[1].plot(output['ATM'], color='orange', label='$Dirac$')
axs[1].set(ylabel='%')
axs[1].legend()
axs[1].grid()

plt.show()
