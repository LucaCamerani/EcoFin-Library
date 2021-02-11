"""
optionGreeksPlot.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import matplotlib.pyplot as plt
import pandas as pd

from EcoFin.options.blackScholesModel import BSM

greeks = {'Delta': [], 'Gamma': [], 'Theta': [], 'Vega': [], 'Rho': []}

strikes = range(1, 200, 1)
data = pd.DataFrame(index=strikes, columns=greeks)
data = data.merge(data, left_index=True, right_index=True, suffixes=['_call', '_put'])

for strike, row in data.iterrows():
    option = BSM(100, strike, 0.05, 0.2, 40)

    data.loc[strike, 'Delta_call'] = option.delta().call
    data.loc[strike, 'Gamma_call'] = option.gamma().call
    data.loc[strike, 'Theta_call'] = option.theta().call
    data.loc[strike, 'Vega_call'] = option.vega().call
    data.loc[strike, 'Rho_call'] = option.rho().call

    data.loc[strike, 'Delta_put'] = option.delta().put
    data.loc[strike, 'Gamma_put'] = option.gamma().put
    data.loc[strike, 'Theta_put'] = option.theta().put
    data.loc[strike, 'Vega_put'] = option.vega().put
    data.loc[strike, 'Rho_put'] = option.rho().put

# create plots with results
for greek in greeks.keys():
    fig, axs = plt.subplots(1, 2, figsize=(12, 4), sharey=True)
    fig.suptitle('{} greek for call and put options by Strike ($K$)'.format(greek))

    axs[0].plot(strikes, data['{}_call'.format(greek)], label=r'${}_C$'.format(greek), color='green')
    axs[0].set(xlabel='Strike', ylabel='Value')
    axs[0].legend()
    axs[0].grid()

    axs[1].plot(strikes, data['{}_put'.format(greek)], label=r'${}_P$'.format(greek), color='red')
    axs[1].set(xlabel='Strike', ylabel='Value')
    axs[1].legend()
    axs[1].grid()

    plt.show()
