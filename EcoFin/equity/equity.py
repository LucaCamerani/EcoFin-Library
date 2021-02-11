"""
equity.py

Created by Luca Camerani at 13/09/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import numpy as np


class Equity():
    def __init__(self, dataFrame, log=False, skipNaN=True):
        self.dataFrame = dataFrame
        self.log = log
        self.skipNaN = skipNaN

    def getReturns(self):
        if self.log:
            return self.dataFrame.pct_change()
        else:
            return self.getLogReturns()

    def getLogReturns(self):
        return np.log(1 + self.getReturns())

    def meanReturn(self, driver=None):
        # [!!!] driver
        return self.getReturns().mean(axis=0, skipna=self.skipNaN)

    def varReturn(self):
        return self.getReturns().var(axis=0, skipna=self.skipNaN)

    def stdReturn(self):
        return np.sqrt(self.varReturn())

    def covMatrix(self):
        return self.getReturns().cov()
