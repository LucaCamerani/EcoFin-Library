"""
montecarloSimulation.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import math
from collections import namedtuple

import numpy as np
from scipy.stats import norm, t

from EcoFin.utils.utils import listInterpreter


class Process():
    def __init__(self, T, dt, t=0, n=None):
        self.T = T
        self.t = t
        self.dt = dt
        self.n = n
        self.steps = self.getStepsN()
        if n is None: self.n = 1

    def getStepsN(self):
        return math.trunc((self.T - self.t) / self.dt) + 1

    def getTimeVector(self):
        return np.arange(self.t, self.T + 1, self.dt)

    def uniformStochasticProcess(self, lineCorr=True):
        output = []
        for i in range(0, self.n):
            output.append(np.random.rand(self.steps))

        if lineCorr: output = listInterpreter(output)
        return output

    def gaussianProcess(self, mean=None, covMatrix=None, lineCorr=True):
        output = []
        for i in range(0, self.n):
            if not mean: meanN = np.full(self.steps, 0)
            if not covMatrix: covMatrixN = np.eye(self.steps)

            output.append(np.random.multivariate_normal(meanN, covMatrixN))

        if lineCorr:
            output = listInterpreter(output)

        return output

    def standardBrownianMotion(self, lineCorr=True):
        output = {'process': [], 'increments': []}
        for i in range(0, self.n):
            x0 = np.asarray(0)
            r = norm.rvs(size=x0.shape + (self.steps - 1,), scale=np.sqrt(self.dt))
            r = np.insert(r, 0, 0)

            out = np.empty(r.shape)

            np.cumsum(r, axis=-1, out=out)
            out += np.expand_dims(x0, axis=-1)

            output['process'].append(out)
            output['increments'].append(r)

        if lineCorr:
            output['process'] = listInterpreter(output['process'])
            output['increments'] = listInterpreter(output['increments'])
        return namedtuple('Output', ['process', 'increments'])(**{
            "process": output['process'],
            "increments": output['increments']
        })

    def tStudentBrownianMotion(self, lineCorr=True, df=1):
        output = {'process': [], 'increments': []}
        for i in range(0, self.n):
            x0 = np.asarray(0)
            r = t.rvs(size=x0.shape + (self.steps - 1,), scale=np.sqrt(self.dt), df=df)
            r = np.insert(r, 0, 0)

            out = np.empty(r.shape)

            np.cumsum(r, axis=-1, out=out)
            out += np.expand_dims(x0, axis=-1)

            output['process'].append(out)
            output['increments'].append(r)

        if lineCorr:
            output['process'] = listInterpreter(output['process'])
            output['increments'] = listInterpreter(output['increments'])

        return namedtuple('Output', ['process', 'increments'])(**{
            "process": output['process'],
            "increments": output['increments']
        })
