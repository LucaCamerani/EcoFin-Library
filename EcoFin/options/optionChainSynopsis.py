"""
optionChainSynopsis.py

Created by Luca Camerani at 11/12/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

from collections import namedtuple

import numpy as np

from EcoFin.options.deepOptionChain import DeepOptionChain
from EcoFin.stat.utils import weightedAvg, weightedStd


class OptionChainSinopsys():
    def __init__(self, deepOptionChain: DeepOptionChain, weights):
        """
        weightsMode:
        * EW -> equally weighted (default);
        * ATM
        * OI -> open interest;
        """
        self.deepOptionChain = deepOptionChain
        self.deepChain = deepOptionChain.getDeepOptionChain()
        self.optionChain = deepOptionChain.getOptionChain()
        self.data = self.deepChain

        self.avaiableIV = deepOptionChain.computeIV
        self.weights = weights

    def computeOptionPriceSpread(self):
        mean = weightedAvg(self.data['spreadSummary'], self.weights)
        std = weightedStd(self.data['spreadSummary'], self.weights)

        return namedtuple('OPS', ['mean', 'std'])(**{
            "mean": mean,
            "std": std
        })

    def computeImpliedVolatilitySpread(self):
        if self.avaiableIV:
            mean = weightedAvg(self.data['IV_spread'], self.weights)
            std = weightedStd(self.data['IV_spread'], self.weights)
        else:
            mean = None
            std = None

        return namedtuple('OPS', ['mean', 'std'])(**{
            "mean": mean,
            "std": std
        })

    def computeNoArbitragePrice(self):
        self.data['S_mean'] = np.mean(self.data[['S_U', 'S_L']], axis=1)
        forecast = np.mean(self.data[['S_U', 'S_L', 'S_mean']])

        return namedtuple('OPS', ['value', 'ret'])(**{
            "value": forecast['S_mean'],
            "ret": forecast['S_mean'] / self.deepOptionChain.getOptionChain().getSpotPrice(),
        })

    def computeOpenInterestRatio(self):
        mean = weightedAvg(self.data['openInterestRatio'], self.weights)
        std = weightedStd(self.data['openInterestRatio'], self.weights)

        return namedtuple('OIR', ['mean', 'std'])(**{
            "mean": mean,
            "std": std
        })

    def computePutCallDelta(self):
        price = self.data.loc[self.data['PutCallDelta'].idxmin(), 'strike']
        PCD = (price / float(self.optionChain.getForwardPrice()) - 1) * 100

        return PCD

    def getWeights(self):
        return self.weights
