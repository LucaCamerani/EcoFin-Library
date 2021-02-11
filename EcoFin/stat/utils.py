"""
utils.py

Created by Luca Camerani at 30/11/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import math

import numpy as np


def weightedAvg(values, weights):
    values = values.fillna(0)
    weights = weights.fillna(0)
    average = np.average(values, weights=weights)

    return average


def weightedStd(values, weights):
    try:
        values = values.fillna(0)
        weights = weights.fillna(0)
        average = weightedAvg(values, weights=weights)
        variance = np.average((values - average) ** 2, weights=weights)

        return math.sqrt(variance)
    except:
        return None
