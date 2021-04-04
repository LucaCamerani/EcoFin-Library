"""
plainVanillaPricing.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import matplotlib.pyplot as plt

from EcoFin.options.binomialTree import BinomialTree

call = []
put = []
strikes = range(0, 200, 5)

for strike in strikes:
    tree = BinomialTree(100, strike, 50, 0.05, 0.2, N=50)
    call.append(tree.computePrice().call)
    put.append(tree.computePrice().put)

plt.plot(strikes, call, label='Call option')
plt.plot(strikes, put, label='Put option')
plt.xlabel('Strike')
plt.ylabel('Option price')
plt.legend()
plt.show()
