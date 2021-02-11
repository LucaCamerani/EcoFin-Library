"""
equityVIX.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

from collections import namedtuple

import numpy as np

from EcoFin.math.utils import findNearest
from EcoFin.options.chainWeights import ChainWeights
from EcoFin.options.deepOptionChain import DeepOptionChain
from EcoFin.stat.equityVolatility import EquityVolatility


class EquityVIX():
    def __init__(self, deepOptionChain: DeepOptionChain, volatilityBack=260):
        self.optionChain = deepOptionChain.getOptionChain()
        self.deepChain = deepOptionChain.getDeepOptionChain()
        self.chainWeights = ChainWeights(self.optionChain)

        if deepOptionChain.computeIV:
            self.smile = self.deepChain.smile
        else:
            self.smile = None

        ticker = self.optionChain.getTicker()
        self.history = ticker.getHistory(end=self.optionChain.getChainDate()).tail(volatilityBack)

    def getHistoricalVolatility(self):
        """
        Historical Volatility (using log-returns)
        """
        series = self.history
        volatility = EquityVolatility(series).meanSigma()

        return volatility

    def getMeanVIX(self):
        """
        Returns the Equally Weighted (EW) volatility smile mean
        """
        weights = self.chainWeights.computeEquallyWeights()

        return self.computeFilteredSmile(weights)

    def getBetaVIX(self, k=.6):
        """
        Returns the Beta-binomial (BetaW) volatility smile mean
        """
        weights = self.chainWeights.computeBetaWeights(k)

        return self.computeFilteredSmile(weights)

    def getOpenInterestVIX(self):
        """
        Returns the Open Interest (OI) volatility smile mean
        """
        weights = self.chainWeights.computeOpenInterestsWeights()

        return self.computeFilteredSmile(weights)

    def getATMVIX(self):
        """
        Returns the Dirac r.v. volatility smile mean
        """
        weights = self.chainWeights.computeATMWeights()

        return self.computeFilteredSmile(weights)

    def computeFilteredSmile(self, weights):
        """
        generic weights vector
        """
        if self.smile is None:
            value = None
        else:
            value = weights.values @ self.smile

        return namedtuple('Output', ['value', 'weights'])(**{
            "value": value,
            "weights": weights
        })

    def getCBOEVIX(self):
        """
        Returns CBOE VIX
        """
        r = self.optionChain.getRiskFreeRate()
        T = self.optionChain.getTimeToMaturity().years
        F = self.optionChain.getForwardPrice()
        K = self.deepChain.strike
        Q = self.deepChain.avgPrice
        K0 = findNearest([i for i in K if i <= F], F)
        delta = K.diff().shift(-1)

        sigma2 = ((2 * np.exp(r * T)) / T) * np.sum(Q / np.square(K) * delta) - (1 / T) * np.square(F / K0 - 1)

        return np.sqrt(sigma2)

    def getVolatilityExcess(self):
        driver = self.getCBOEVIX()
        historical = self.getHistoricalVolatility()

        return driver - historical
