"""
interpolation.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import numpy as np


def interpolateNaN(y):
    """
    :param y: list of values to be interpoled
    :type y: list
    :return: vector of values interpoled
    :rtype: np.array
    """
    if sum(np.isnan(y).astype(int)) != len(y):
        y = np.array(y)
        nans = np.isnan(y)
        x = lambda z: z.nonzero()[0]
        y[nans] = np.interp(x(nans), x(~nans), y[~nans])

    return y
