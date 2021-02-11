"""
itoProcess.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import math

import numpy as np

from EcoFin.math.stochasticProcess.process import Process
from EcoFin.utils.utils import listInterpreter


class ItoProcess():
    def __init__(self, T, dt, t=0, x0=0, n=None):
        self.T = T
        self.t = t
        self.dt = dt
        self.steps = len(self.getTimeVector())
        self.x0 = x0
        self.n = n
        if n is None: self.n = 1

        self.initSBM()

    def getStepsN(self):
        return math.trunc((self.T - self.t) / self.dt) + 1

    def initSBM(self):
        self.SBM = Process(self.T, self.dt, self.t, n=self.n).standardBrownianMotion(lineCorr=False)
        return self.SBM

    def getTimeVector(self):
        return np.arange(self.t, self.T + 1, self.dt)

    def driftBrownianMotion(self, a, b, scalarCorr=True):
        self.initSBM()
        output = []
        for i in range(0, self.n):
            dX = a * self.dt + b * self.SBM.increments[i]
            output.append(self.x0 + np.cumsum(dX))

        if scalarCorr: output = listInterpreter(output)
        return output

    def geometricBrownianMotion(self, mu, sigma, scalarCorr=True):
        self.initSBM()
        output = []
        for i in range(0, self.n):
            x = [self.x0]
            for k in range(1, self.getStepsN()):
                drift = (mu - .5 * sigma ** 2) * (self.getTimeVector() - self.t)[k]
                diffusion = sigma * self.SBM.process[i][k]
                temp = self.x0 * np.exp(drift + diffusion)
                x.append(temp)

            output.append(x)

        if scalarCorr: output = listInterpreter(output)
        return output

    def meanRevertingProcess(self, k, theta, sigma):
        """
        :param k: mean reversion force
        :type k:
        :param theta: long term value
        :type theta:
        :param sigma:
        :type sigma:
        :return:
        :rtype:
        """
        self.initSBM()
        longTerm = theta - self.x0
        sigmaBis = sigma * np.sqrt(2. / k)
        x = np.zeros(self.steps)
        for i in range(self.steps - 1):
            x[i + 1] = x[i] + k * (longTerm - x[i]) * self.dt + \
                       sigmaBis * self.SBM.increments[i]

        return self.x0 + x
