"""
allocation.py

Created by Luca Camerani at 10/02/2021, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import numpy as np
import pandas as pd

from collections import namedtuple


class Allocation():
    def __init__(self, signals: pd.DataFrame, buyOnly=False, limit=None, unit=1):
        self.unit = unit
        self.signals = signals

        if limit is not None:
            self.signals = self.filterWeights(limit)

        if buyOnly:
            self.signals[self.signals < 0] = 0

    def getEquallyWeights(self):
        weights = (1 - pd.isnull(self.signals)).\
            div(self.signals.count(axis=1).values, axis=0)

        return weights

    def getSignalWeights(self):
        weights = self.signals.div(self.signals.abs().sum(axis=1), axis=0)

        return weights

    def filterWeights(self, z: int):
        base = self.signals.copy()

        m = base.apply(lambda x: x.fillna(0).sort_values()[-z], axis=1)
        r = base[base.ge(m, axis=0)]

        return r

    # Portfolio composition informations

    def countAssets(self, weights: pd.DataFrame):
        return weights.fillna(0).ne(0).sum(axis=1)

    def getBalancing(self, weights: pd.DataFrame):
        return weights.sum(axis=1)

    def getTurnover(self, weights: pd.DataFrame):
        turnover = np.abs(weights.shift(1, axis=1) - weights)

        return namedtuple('Turnover', ['matrix', 'byTime', 'byTicker', 'mean'])(**{
            "matrix": turnover,
            "byTime": turnover.mean(axis=1),
            "byTicker": turnover.mean(),
            "mean": np.nanmean(turnover.values)
        })
