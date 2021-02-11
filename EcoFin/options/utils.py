"""
equity.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

from datetime import datetime

import numpy as np


def daysDifference(fromDate, toDate):
    if isinstance(fromDate, (int, float, datetime)):
        fromDate = [fromDate]
    if isinstance(toDate, (int, float, datetime)):
        toDate = [toDate]
    fromDate = np.array(fromDate)
    toDate = np.array(toDate)

    if not isinstance(fromDate[0], datetime):
        fromDate = np.array([datetime.fromtimestamp(dte) for dte in fromDate])

    if not isinstance(toDate[0], datetime):
        toDate = np.array([datetime.fromtimestamp(dte) for dte in toDate])

    diff = (toDate - fromDate)

    if len(diff) == 1:
        return float(diff[0].total_seconds() / 86400)
    else:
        return np.array([float(delta.total_seconds()) for delta in diff]) / 86400


def daysToMaturity(expirations, fromDate=None):
    if fromDate is None:
        fromDate = datetime.now()
    return daysDifference(fromDate, expirations)


def daysFromLastDate(lastDate, expirations):
    return -daysToMaturity(lastDate, expirations)
