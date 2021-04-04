"""
americanOptionPricig.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

from EcoFin.options.binomialTree import BinomialTree

tree = BinomialTree(30, 29, 40, 0.05, 0.3, N=8, plainVanilla=False, div=0)

print(tree.getPayoffAtTime(step=7).put)
print(tree.computePrice())
