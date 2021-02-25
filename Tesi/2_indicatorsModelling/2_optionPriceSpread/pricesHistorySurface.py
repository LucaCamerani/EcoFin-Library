"""
pricesHistorySurface.py

Created by Luca Camerani at 21/01/2021, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tqdm

from mpl_toolkits.mplot3d import axes3d
from EcoFin.dataDownload.optionsManager import OptionManager
from EcoFin.dataDownload.ticker import Ticker
from EcoFin.options.deepOptionSurface import DeepOptionSurface
from EcoFin.options.utils import daysToMaturity

# ---------------------------[Set-Up]--------------------------------
ticker = Ticker('MSFT')

increment = 86400  # 1 day
date1 = 1551657600  # Monday 4 March 2019
date2 = date1 + increment * 1
# -------------------------------------------------------------------

for now in tqdm.tqdm(range(date1, date2, increment), desc='Generate frames'):  # Compute day by day
    try:
        optionManager = OptionManager(ticker, now=now)
        optSurface = optionManager.getOptionSurface()
        deepSurface = DeepOptionSurface(optSurface, computeIV=False, computeBSM=False, progressBar=False)

        # get IV surface data
        exps = optSurface.getExpirations()

        fig = plt.figure(figsize=(15, 10))
        fig.suptitle('Option Prices Spread Analysis', fontsize=16)

        # Plot option price surfaces
        ax = fig.add_subplot(211, projection='3d')
        ax.set_title('Option Prices Surfaces')

        forwardP = {}
        output = {'call': {}, 'put': {}, 'OPS': {}}
        for exp in exps[1:6]:
            surfaceChain = deepSurface.getDeepChainByDate(exp)
            chain = surfaceChain.getDeepOptionChain().set_index('strike')
            tau = daysToMaturity(exp, optSurface.getDate())

            output['call'][tau] = chain['avgPrice_call']
            output['put'][tau] = chain['avgPrice_put']
            output['OPS'][tau] = chain['spreadSummary']
            forwardP[tau] = surfaceChain.getOptionChain().getForwardPrice()

        # Convert data to a dataframe (merging concat) and interpolate NaN
        forwardP = pd.Series(forwardP)
        for key, data in output.items():
            output[key] = pd.concat(data, axis=1).interpolate(limit_direction='both', axis=0)

        X, Y = np.meshgrid(output['OPS'].keys(), output['OPS'].index)

        c = ax.plot_surface(X, Y, output['call'], alpha=.7, cmap='Greens', linewidth=1)
        c = ax.plot_surface(X, Y, output['put'], alpha=.7, cmap='Reds', linewidth=1)
        c._facecolors2d = c._facecolors3d

        ax.set_xlabel(r'Strike ($K$)')
        ax.set_ylabel(r'Days to maturity ($\tau$)')
        ax.set_zlabel(r'Prices')
        ax.view_init(elev=20., azim=-180)

        # Plot option price spread surface
        ax = fig.add_subplot(223)
        cmap = plt.cm.get_cmap("winter")

        ax.set_title('Option Price Spread')
        c = ax.contourf(Y, X, output['OPS'], 50, cmap=cmap)
        ax.set_xlabel(r'Strike ($K$)')
        ax.set_ylabel(r'Days to maturity ($\tau$)')
        ax.plot(forwardP.values, forwardP.index, linestyle="dashed", color='white', alpha=1, label='Forward Price')
        ax.legend()

        plt.colorbar(c)

        # Plot underlying price
        ax = fig.add_subplot(224)
        ax.set_title('Underlying prices')

        # Get underlying price history
        history_back = 30
        history = ticker.getHistory(end=now).tail(history_back)
        ax.plot(history.Close)

        plt.show()

        # Save frame
        # ----------------------[EXPORT BLOCK]--------------------------------
        path = r'../../../Export/{}'.format(ticker.ticker)
        if not os.path.exists(path):
            os.makedirs(path)

        plt.savefig(r'{}/{}_{}.png'.format(path, now, ticker.ticker))
        # ----------------------[EXPORT BLOCK]--------------------------------
    except:
        print('Error: {}'.format(now))
        pass
