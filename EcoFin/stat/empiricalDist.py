"""
empiricalDist.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

from statistics import mode

import numpy as np


def rescaleData(data):
    return data / np.full(len(data), sum(data))


def normalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))


def getClassSize(data):
    xdiff = [data[n] - data[n - 1] for n in range(1, len(data))]
    xdiff.insert(0, mode(xdiff))

    return xdiff


def cdfTopdf(data):
    xdiff = [data[n] - data[n - 1] for n in range(1, len(data))]
    xdiff.insert(0, np.nan)
    return xdiff
