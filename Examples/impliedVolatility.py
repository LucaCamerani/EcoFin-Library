"""
impliedVolatility.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import time

from EcoFin.options.blackScholesModel import BSM

marketPrice = 3
option = BSM(100, 100, 0.05, 0.2, 70)

start_time = time.time()  # [START]

print(option.getImpliedVolatility(marketPrice, 'call'))

print('chrono: ' + str(time.time() - start_time))  # [STOP]
