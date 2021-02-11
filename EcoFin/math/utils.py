"""
equity.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import numpy as np


def findNearest(array, value):
    if sum(np.isnan(array)) == len(array):
        return None
    else:
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]
