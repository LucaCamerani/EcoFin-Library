"""
equity.py

Created by Luca Camerani at 02/09/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

from datetime import datetime

import numpy as np
import pandas as pd


def listInterpreter(data):
    data = np.array(data)
    if len(data) == 1:
        data = data[0]

    return data


def date_to_unixtimestamp(date: (int, str)):
    date = (pd.to_datetime(date, format='%Y%m%d') - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')

    return date


def unixtimestamp_to_date(date: (int, str)):
    date = datetime.utcfromtimestamp(int(date)).strftime('%Y%m%d')

    return date


def polarizeTable(data: pd.DataFrame, cutoff=0, over=1, under=-1):
    """
    This function returns a polarized matrix (dataframe)
    """
    table = data.copy()
    table[table > cutoff] = over
    table[table < cutoff] = under

    return table


def filterTable(data: pd.DataFrame, confidence=.1):
    """
    This function returns the extremes value of dataframe
    """
    table = pd.DataFrame().reindex_like(data)

    l = data.quantile(confidence)
    h = data.quantile(1 - confidence)

    table[data.ge(h, axis=1)] = data
    table[data.le(l, axis=1)] = data

    return table
