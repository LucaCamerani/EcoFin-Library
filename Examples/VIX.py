"""
VIX.py

Created by Luca Camerani at 24/09/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

from EcoFin.dataDownload.optionsManager import OptionManager
from EcoFin.dataDownload.ticker import Ticker
from EcoFin.options.deepOptionChain import DeepOptionChain
from EcoFin.options.equityVIX import EquityVIX

# -------------------------[Set-up]-------------------------
ticker = Ticker('MSFT')
optionManager = OptionManager(ticker, now=None)

i = 0  # <- Time To Maturity curve
exp = optionManager.getExpirations()[i]

optionChain = optionManager.getOptionChain(exp=exp)
# ----------------------------------------------------------

deepOptionChain = DeepOptionChain(optionChain)
equityVIX = EquityVIX(deepOptionChain)

VIX = {'MeanVIX': equityVIX.getMeanVIX().value,
       'BetaVIX': equityVIX.getBetaVIX().value,
       'CBOEVIX': equityVIX.getCBOEVIX(),
       'Historical': equityVIX.getHistoricalVolatility(),
       'VE': equityVIX.getVolatilityExcess()}

print('\n---------------------------')
print(' • Mean VIX: {}'.format(VIX['MeanVIX']))
print(' • Beta VIX: {}'.format(VIX['BetaVIX']))
print(' • CBOE VIX: {}'.format(VIX['CBOEVIX']))
print(' • Historical volatility: {}'.format(VIX['Historical']))
print(' • Volatility Excess (VE): {}'.format(VIX['VE']))
print('---------------------------\n')
