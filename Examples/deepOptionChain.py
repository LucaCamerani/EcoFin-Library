"""
deepOptionChain.py

Created by Luca Camerani at 23/12/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import pandas as pd

from EcoFin.dataDownload.optionsManager import OptionManager
from EcoFin.dataDownload.ticker import Ticker
from EcoFin.options.deepOptionChain import DeepOptionChain

# -------------------------[Set-up]-------------------------
ticker = Ticker('MSFT')
optionManager = OptionManager(ticker, now=None)

i = 0  # <- Time To Maturity curve
exp = optionManager.getExpirations()[i]

optionChain = optionManager.getOptionChain(exp=exp)
# ----------------------------------------------------------

chain = optionChain.getChain()
deepChain = DeepOptionChain(optionChain).getDeepOptionChain()

path = '../Export/[{}]_deepOptionChain.xlsx'.format(ticker.ticker)
with pd.ExcelWriter(path) as writer:
    chain.full.to_excel(writer, sheet_name='Chain')
    deepChain.to_excel(writer, sheet_name='Deep Chain')

print('file saved! ({})'.format(path))
