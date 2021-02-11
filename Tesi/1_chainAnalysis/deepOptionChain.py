"""
1_deepOptionChain.py

Created by Luca Camerani at 22/11/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import os

import pandas as pd

from EcoFin.dataDownload.optionsManager import OptionManager
from EcoFin.dataDownload.ticker import Ticker
from EcoFin.options.deepOptionChain import DeepOptionChain

# -------------------------[Set-up]-------------------------
ticker = Ticker('MSFT')
optionManager = OptionManager(ticker)
exp = optionManager.getExpirationByMaturity(30, method='greater')
optionChain = optionManager.getOptionChain(exp=exp)
# ----------------------------------------------------------

ticker_info = ticker.getInfo()
forwardPrice = optionChain.getForwardPrice()

deepOptionChain = DeepOptionChain(optionChain, computeIV=False)
data = deepOptionChain.getDeepOptionChain()

# ----------------------[EXPORT BLOCK]--------------------------------
path = '../Export/[{}]'.format(ticker.ticker)
if not os.path.exists(path):
    os.makedirs(path)
with pd.ExcelWriter('{}/deepOptionChain_[{}].xlsx'.format(path, exp)) as writer:
    data.to_excel(writer, sheet_name='Chain', index=False)

print('\nFile saved!')
# ----------------------[EXPORT BLOCK]--------------------------------
