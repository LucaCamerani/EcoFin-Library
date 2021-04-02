"""
optionGreeks.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

from EcoFin.options.blackScholesModel import BSM

option = BSM(100, 100, 0.05, 0.2, 70)

print(option.computeValues())
# -----
print(option.computePrice())
print('Greeks:')
print(' • {}'.format(option.delta()))
print(' • {}'.format(option.gamma()))
print(' • {}'.format(option.theta()))
print(' • {}'.format(option.vega()))
print(' • {}'.format(option.rho()))
