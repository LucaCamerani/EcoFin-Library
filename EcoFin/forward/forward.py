"""
forward.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import numpy as np


class Forward():
    def __init__(self, S, r, daysToMaturity, div=0):
        self.T = daysToMaturity / float(365)
        self.S = S
        self.div = div
        self.r = r
        if r is None: self.r = 0

    def getForwardPrice(self):
        return self.S * np.exp((self.r - self.div) * self.T)
