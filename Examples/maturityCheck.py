"""
maturityCheck.py

Created by Luca Camerani at 18/12/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

from EcoFin.dataDownload.optionsManager import OptionManager
from EcoFin.dataDownload.ticker import Ticker

# -------------------------[Set-up]-------------------------
ticker = Ticker('MSFT')

# 1Y
increment = 86400
maturity = 30
date1 = 1546300800
date2 = 1577664000
# ----------------------------------------------------------

optionManager = OptionManager(ticker)
ticker_info = ticker.getInfo()

for now in range(date1, date2, increment):  # Compute day by day
    try:
        optionManager.setNow(now)

        exp = optionManager.getExpirationByMaturity(maturity, 'greater')
        optionChain = optionManager.getOptionChain(exp=exp)

        print('Maturity: {} days'.format(optionChain.getTimeToMaturity().days))
    except:
        pass
