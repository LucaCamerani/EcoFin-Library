"""
chainWeights.py

Created by Luca Camerani at 04/01/2021, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import numpy as np
import pandas as pd
from scipy.stats import betabinom

from EcoFin.options.deepOptionChain import DeepOptionChain
from EcoFin.options.optionChain import OptionChain


class ChainWeights():
    def __init__(self, optionChain: (OptionChain, DeepOptionChain)):
        if isinstance(optionChain, OptionChain):
            self.optionChain = optionChain
            self.deepOptionChain = None
        elif isinstance(optionChain, DeepOptionChain):
            self.optionChain = optionChain.getOptionChain()
            self.deepOptionChain = optionChain

        self.data = optionChain.getChain().full

    def computeEquallyWeights(self):
        weights = pd.Series(np.full(self.data.shape[0], 1 / self.data.shape[0]), index=self.optionChain.getStrikeList())

        return weights

    def computeATMWeights(self):
        moneyness = self.data['moneyness'].abs()
        weights = moneyness.eq(moneyness.where(moneyness != 0).min()).astype(int)
        weights = pd.Series(weights.values, index=self.optionChain.getStrikeList())

        return weights

    def computeOpenInterestsWeights(self):
        weights = self.data.loc[:, ['openInterest_call', 'openInterest_put']].sum(axis=1) / \
                  np.nansum(self.data.loc[:, ['openInterest_call', 'openInterest_put']].to_numpy())
        weights = pd.Series(weights.values, index=self.optionChain.getStrikeList())

        return weights

    def computeBetaWeights(self, k=.6):
        strikeList = self.optionChain.getStrikeList()
        n = len(strikeList)
        x = np.arange(0, n)

        weights = betabinom.pmf(x, n - 1, k, k)
        weights = pd.Series(weights, index=self.optionChain.getStrikeList())

        return weights

    def computeMoneynessWeights(self):
        moneyness = self.data['moneyness'].max() - np.abs(self.data['moneyness'])
        weights = moneyness / np.sum(moneyness)
        weights = pd.Series(weights.values, index=self.optionChain.getStrikeList())

        return weights
