"""
2_correlationTester.py

Created by Luca Camerani at 19/01/2021, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import numpy as np
import pandas as pd
from tqdm import tqdm

from EcoFin.utils import utils

# -------------------------[Set-up]-------------------------
ticker_list = [line.rstrip('\n') for line in open(r'../INDEXs/DJIA.txt')]
maturity_min = 15

base_path = r'../Export/BackTest'
start_date = 0

direction = {'OPS': ['EW', 'OI', 'Beta', 'ATM', 'Moneyness']}
force = {'VIX': ['hist', 'mean', 'beta', 'CBOE']}
# ----------------------------------------------------------

data = {'base': {'Maturity': {}, 'SpotPrice': {}},
        'direction': {'{}_[{}]'.format(list(direction)[0], d): {} for d in direction[list(direction)[0]]},
        'force': {'{}_[{}]'.format(list(force)[0], f): {} for f in force[list(force)[0]]}}

for tick in tqdm(ticker_list, desc='Preprocessing data'):
    try:
        # Import data and clean-up
        source = pd.read_excel(r'{}/{}/backTest_[{}].xlsx'.format(base_path, tick, maturity_min), engine='openpyxl')
        source = source.loc[source['Date'] >= start_date, ~source.columns.str.contains('^Unnamed')]
        source.set_index(pd.to_datetime(source['Date'], format='%Y%m%d'), drop=True, inplace=True)

        for group in data.keys():
            for driver in data[group].keys():
                data[group][driver][tick] = source[driver]
    except:
        pass

# Merge (concatenate) data and create dataframes
for group in data.keys():
    for driver in data[group].keys():
        data[group][driver] = pd.concat(data[group][driver], axis=1)

        # ❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌[Normalize direction data]❌❌❌❌❌❌❌❌❌❌❌
        if group == 'direction':
            data[group][driver] = data[group][driver].sub(data[group][driver].mean(axis=1), axis=0)
        # ❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌

# Compute ln-returns table
data['base']['lnReturns'] = np.log(data['base']['SpotPrice'].shift(-1) / data['base']['SpotPrice'])
data['base']['extraReturns'] = data['base']['lnReturns'].sub(data['base']['lnReturns'].mean(axis=1), axis=0)

# Perform correlation analysis
on = 'extraReturns'
data['correlation'] = {'linear': {},
                       'polarized': {},
                       'quantile': {},
                       'absolute': {}}

# [1] Linear Correlation (LC)
for group in ['direction', 'force']:
    for driver in data[group].keys():
        data['correlation']['linear'][driver] = data[group][driver].corrwith(data['base'][on])
data['correlation']['linear'] = pd.concat(data['correlation']['linear'], axis=1)

# [2] Polarized Correlation (PC)
on_tab = utils.polarizeTable(data['base'][on])
for group in ['direction', 'force']:
    for driver in data[group].keys():
        table = utils.polarizeTable(data[group][driver], cutoff=0)

        data['correlation']['polarized'][driver] = table.corrwith(on_tab)

data['correlation']['polarized'] = pd.concat(data['correlation']['polarized'], axis=1)

# [3] Quantile Correlation (QC)
on_tab = data['base'][on]
for group in ['direction', 'force']:
    for driver in data[group].keys():
        table = utils.filterTable(data[group][driver])
        data['correlation']['quantile'][driver] = table.corrwith(on_tab)

data['correlation']['quantile'] = pd.concat(data['correlation']['quantile'], axis=1)

# [4] Absolute Correlation (AC)
on_tab = data['base'][on].abs()
for group in ['direction', 'force']:
    for driver in data[group].keys():
        table = data[group][driver].abs()
        data['correlation']['absolute'][driver] = table.corrwith(on_tab)

data['correlation']['absolute'] = pd.concat(data['correlation']['absolute'], axis=1)

# ----------------------[EXPORT BLOCK]--------------------------------
with pd.ExcelWriter('{}/{}_CA_[{}].xlsx'.format(base_path, list(direction)[0], maturity_min)) as writer:
    for group, keys in {a: x.keys() for a, x in data.items()}.items():
        for driver in keys:
            try:
                data[group][driver].to_excel(writer, sheet_name=driver.replace('[', '(').replace(']', ')'))
            except:
                pass

print('\nFile saved!')
# ----------------------[EXPORT BLOCK]--------------------------------
