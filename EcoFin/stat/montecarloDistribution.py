"""
montecarloDistribution.py

Created by Luca Camerani at 02/09/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

from collections import namedtuple

import numpy as np
from sklearn.neighbors import KernelDensity


class MonteCarlo():
    def __init__(self, simulation):
        self.simulation = simulation

    def getIndexSpace(self):
        return np.arange(0, self.simulation.shape[1])

    def getProcessList(self):
        return self.simulation

    def getData(self, index=None):
        if index is None: index = self.getIndexSpace()[-1]

        return self.simulation[:, index]

    def getValues(self, step=1, index=None):
        if index is None:
            bounds = {'min': [], 'max': []}
            for k in self.getIndexSpace():
                data = self.getData(index=k)
                bounds['min'].append(np.amin(data))
                bounds['max'].append(np.amax(data))
            bounds = {'min': min(bounds['min']), 'max': max(bounds['max'])}
        else:
            hist = self.getData(index=index)
            bounds = {'min': np.amin(hist), 'max': np.amax(hist)}

        values = np.asarray([value for value in np.arange(int(bounds['min']), int(bounds['max']) + 1, step)])
        values = values.reshape((len(values), 1))

        return values

    def getEmpiricalDist(self, index=None, step=1, bandwidth=5, fullSpace=False):
        model = KernelDensity(bandwidth=bandwidth, kernel='gaussian')
        hist = self.getData(index=index)
        sample = hist.reshape((len(hist), 1))
        model.fit(sample)

        if fullSpace:
            values = self.getValues(step=step)
        else:
            values = self.getValues(step=step, index=index)

        probabilities = np.exp(model.score_samples(values))

        return namedtuple('Density', ['values', 'probabilities'])(**{
            "values": values,
            "probabilities": probabilities
        })

    def getEmpiricalCumulativeDist(self, index=None, step=1, bandwidth=5, fullSpace=False):
        PDF = self.getEmpiricalDist(index=index, step=step, bandwidth=bandwidth, fullSpace=fullSpace)

        return namedtuple('Density', ['values', 'probabilities'])(**{
            "values": PDF.values,
            "probabilities": np.cumsum(PDF.probabilities)
        })
