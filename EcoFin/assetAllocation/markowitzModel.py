"""
markowitzModel.py

Created by Luca Camerani at 13/09/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

from collections import namedtuple

import numpy as np
import scipy.optimize as sco

from EcoFin.equity.equity import Equity


class MarkowitzModel():
    def __init__(self, marketDataFrame, log=True):
        self.dataFrame = marketDataFrame
        self.equity = Equity(marketDataFrame, log=log)
        self.mean = np.array(self.equity.meanReturn())
        self.cov = self.equity.covMatrix().to_numpy()
        self.numAssets = len(self.mean)

    def computeEfficientFrontier(self, returnSpace=np.arange(0, 1, .1)):
        frontier = []
        for i in returnSpace:
            weights = self.efficientReturn(target=i)
            if weights is not None:
                frontier.append(weights)

        return frontier

    def portfolioPerformance(self, weights, annualize=True, r=0):
        days = 1
        if annualize: days = 260

        ret = np.dot(weights.T, self.mean) * days
        std = np.sqrt(np.dot(weights, np.dot(self.cov * days, weights.T)))
        SR = (ret - r) / std

        return namedtuple('Performance', ['std', 'ret', 'SR'])(**{
            "std": std,
            "ret": ret,
            "SR": SR
        })

    def portfolioVolatility(self, weights, *args):
        return self.portfolioPerformance(weights).std

    def efficientReturn(self, target):
        args = (self.mean, self.cov)

        def portfolioReturn(weights):
            return self.portfolioPerformance(weights).ret

        constraints = ({'type': 'eq', 'fun': lambda x: portfolioReturn(x) - target},
                       {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for asset in range(self.numAssets))
        result = sco.minimize(self.portfolioVolatility, self.numAssets * [1. / self.numAssets, ], args=args,
                              method='SLSQP',
                              bounds=bounds, constraints=constraints)

        if result['success'] is np.bool_(True):
            return result['x']
        else:
            return None

    def randomWeights(self, N):
        weights = []
        for i in range(0, N):
            rand = np.random.rand(self.numAssets)
            weights.append(rand / sum(rand))
        return np.array(weights)

    def getSharpeRatio(self, weights, r=0):
        p = self.portfolioPerformance(weights)
        return
