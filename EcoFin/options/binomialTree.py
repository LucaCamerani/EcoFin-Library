"""
binomialTree.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

from collections import namedtuple

import numpy as np
import scipy.stats as ss


class OptionTree():
    def __init__(self, S, K, daysToMaturity, r, sigma, div=0, N=30, plainVanilla=True):
        self.T = daysToMaturity / float(365)
        self.deltaT = float(self.T) / float(N)
        self.u = np.exp(sigma * np.sqrt(self.deltaT))
        self.d = 1 / self.u
        self.r = (r - div)
        self.q = self.getRiskNeutralProb()
        self.S = S
        self.K = K
        self.N = N
        self.plainVanilla = plainVanilla

    def getUnderlyingAtTime(self, step=None):
        if step is None: step = self.N

        prices = []
        for i in range(0, step + 1):
            prices.append(self.S * self.u ** i * self.d ** (step - i))
        return np.array(prices)

    def getRiskNeutralProb(self):
        return (np.exp(self.r * self.deltaT) - self.d) / float(self.u - self.d)

    def getProbabilitiesAtTime(self, step=None):
        if step is None: step = self.N

        probs = []
        q = self.getRiskNeutralProb()
        binomial = ss.binom(step, q)
        for i in range(0, step + 1):
            probs.append(binomial.pmf(i))
        return np.array(probs)

    def getPayoffAtTime(self, step=None):
        if step is None: step = self.N

        callPayoff = self.getUnderlyingAtTime(step=step) - self.K
        callPayoff[callPayoff < 0] = 0

        putPayoff = self.K - self.getUnderlyingAtTime(step=step)
        putPayoff[putPayoff < 0] = 0

        return namedtuple('Payoff', ['call', 'put'])(**{
            "call": callPayoff,
            "put": putPayoff
        })

    def getExerciseProb(self):
        output = {'call': None, 'put': None}
        for type in output.keys():
            if type == 'call':
                payoff = self.getPayoffAtTime().call
            else:
                payoff = self.getPayoffAtTime().put

            payoff[payoff > 0] = 1
            output[type] = sum(self.getProbabilitiesAtTime() * payoff)

        return namedtuple('Probability', ['call', 'put'])(**{
            "call": output['call'],
            "put": output['put']
        })

    def computePrice(self):
        if self.plainVanilla:
            callPrice = np.exp(-self.r * self.T) * np.array(self.getPayoffAtTime().call).dot(
                self.getProbabilitiesAtTime())
            putPrice = np.exp(-self.r * self.T) * np.array(self.getPayoffAtTime().put).dot(
                self.getProbabilitiesAtTime())
        else:
            prices = self.computeAmericanPrice()
            callPrice = prices.call
            putPrice = prices.put

        return namedtuple('Prices', ['call', 'put'])(**{
            "call": callPrice,
            "put": putPrice
        })

    def putCallParity(self, callPrice):
        return callPrice - self.S + self.K * np.exp(-self.r * self.T)

    def computeAmericanPrice(self):
        output = {}
        for type in ['call', 'put']:
            if type == 'call':
                payoff = self.getPayoffAtTime().call
            else:
                payoff = self.getPayoffAtTime().put

            for step in self.getTimeVector():
                price = []
                for node in range(0, len(payoff) - 1, 1):
                    up = payoff[node + 1]
                    down = payoff[node]
                    price.append(np.exp(-self.r * self.deltaT) * (self.q * up + (1 - self.q) * down))

                if type == 'call':
                    backward = self.getPayoffAtTime(step=step).call
                else:
                    backward = self.getPayoffAtTime(step=step).put

                payoff = np.maximum(backward, price)
            output[type] = payoff[0]

        return namedtuple('Prices', ['call', 'put'])(**{
            "call": output['call'],
            "put": output['put']
        })

    def getTimeVector(self):
        return range(self.N - 1, -1, -1)
