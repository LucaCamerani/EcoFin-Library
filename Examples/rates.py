"""
rates.py

Created by Luca Camerani at 14/10/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import pandas as pd

from EcoFin.dataDownload.rates import Rates

r = Rates()

path = '../Export/riskFreeRate.xlsx'
with pd.ExcelWriter(path) as writer:
    # DTB3      -> T Bill Yeld 3M
    # DSG3MO    -> LIBOR 3M
    r.getHistory(code='DTB3').to_excel(writer)

print('file saved! ({})'.format(path))
