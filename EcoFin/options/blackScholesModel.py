"""
blackScholesModel.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

from collections import namedtuple

import numpy as np
from scipy.special import ndtr
from scipy.stats import norm

from EcoFin.math.utils import findNearest


class BSM():
    def __init__(self, S, K, daysToMaturity, r, sigma, div=0):
        self.K = K
        self.r = r
        if r is None: self.r = 0
        self.sigma = sigma
        if sigma == 0: self.sigma = 1.0e-5
        self.T = max(daysToMaturity, 0) / float(365)
        self.S = S * np.exp(-div * self.T)

        if K is not None and sigma is not None:
            val = self.computeValues()
            self.d1 = val.d1
            self.d2 = val.d2

    def computeValues(self, strike=None, sigma=None):
        if sigma is None: sigma = self.sigma
        if strike is None: strike = self.K

        d1 = (np.log(self.S / strike) + (self.r + sigma ** 2 * 0.5) * self.T) / float(sigma * np.sqrt(self.T))
        d2 = d1 - sigma * np.sqrt(self.T)

        return namedtuple('Values', ['d1', 'd2'])(**{
            "d1": d1,
            "d2": d2
        })

    def computePrice(self, sigma=None):
        if sigma == 0: sigma = 1.0e-5
        if sigma is None:
            d1 = self.d1
            d2 = self.d2
        else:
            d1 = self.computeValues(sigma=sigma).d1
            d2 = self.computeValues(sigma=sigma).d2

        output = {'call': self.S * ndtr(d1) - self.K * np.exp(-self.r * self.T) * ndtr(d2),
                  'put': None}
        output['put'] = self.putCallParity(output['call'])

        return namedtuple('Prices', ['call', 'put'])(**{
            "call": output['call'],
            "put": output['put']
        })

    def putCallParity(self, callPrice):
        return callPrice - self.S + self.K * np.exp(-self.r * self.T)

    def getImpliedVolatility(self, marketPrice, type):
        if marketPrice is np.nan:
            res = np.nan
        else:
            range = {'min': 0, 'max': 10}

            space = np.exp(np.linspace(0, -6, 5))
            for precision in space:
                prices = []
                IVs = np.arange(range['min'], range['max'], precision)
                for iv in IVs:
                    if type == 'call':
                        priceIV = self.computePrice(sigma=iv).call
                    else:
                        priceIV = self.computePrice(sigma=iv).put

                    prices.append(priceIV)

                query = findNearest(prices, marketPrice)

                if query is None:
                    res = np.nan
                else:
                    res = IVs[prices.index(query)]
                    range['min'] = np.amax([res - precision, 0])
                    range['max'] = res + precision

        if res == 0:
            res = np.nan

        return res

    # Greeks
    def delta(self):
        deltaCall = ndtr(self.d1)
        deltaPut = deltaCall - 1

        return namedtuple('Delta', ['call', 'put'])(**{
            "call": deltaCall,
            "put": deltaPut
        })

    def gamma(self):
        gammaCall = norm._pdf(self.d1) / float(self.S * self.sigma * np.sqrt(self.T))
        gammaPut = gammaCall

        return namedtuple('Gamma', ['call', 'put'])(**{
            "call": gammaCall,
            "put": gammaPut
        })

    def theta(self):
        thetaCall = -self.K * self.r * np.exp(-self.r * self.T) * ndtr(self.d2) - (
                    self.sigma * self.S * norm._pdf(self.d1) / (2 * np.sqrt(self.T)))
        thetaPut = self.K * self.r * np.exp(-self.r * self.T) + thetaCall

        return namedtuple('Theta', ['call', 'put'])(**{
            "call": thetaCall,
            "put": thetaPut
        })

    def vega(self):
        vegaCall = self.S * norm._pdf(self.d1) * np.sqrt(self.T)
        vegaPut = vegaCall

        return namedtuple('Vega', ['call', 'put'])(**{
            "call": vegaCall,
            "put": vegaPut
        })

    def rho(self):
        rhoCall = self.K * self.T * np.exp(-self.r * self.T) * ndtr(self.d2)
        rhoPut = rhoCall - self.K * np.exp(-self.r * self.T) * self.T

        return namedtuple('Rho', ['call', 'put'])(**{
            "call": rhoCall,
            "put": rhoPut
        })

    def omega(self):
        omegaCall = None
        omegaPut = None

        return namedtuple('Rho', ['call', 'put'])(**{
            "call": omegaCall,
            "put": omegaPut
        })

    def theoreticalDistribution(self, strikes):
        probability = []
        for strike in strikes:
            probability.append(norm._pdf(self.computeValues(strike=strike).d2))

        return namedtuple('Distruibution', ['strike', 'probability'])(**{
            "strike": strikes,
            "probability": probability
        })
