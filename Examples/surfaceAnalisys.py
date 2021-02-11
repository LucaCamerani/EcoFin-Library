"""
surfaceAnalisys.py

Created by Luca Camerani at 11/12/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

from EcoFin.dataDownload.optionsManager import OptionManager
from EcoFin.dataDownload.ticker import Ticker

ticker = Ticker('MSFT')
ticker_info = ticker.getInfo()

optionManager = OptionManager(ticker, now=None)
optionSurface = optionManager.getOptionSurface()

print(optionSurface.getChainByMaturity(30))
