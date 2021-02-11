"""
impliedVolatility.py

Created by Luca Camerani at 18/10/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import time

import matplotlib.pyplot as plt

from EcoFin.dataDownload.optionsManager import OptionManager
from EcoFin.dataDownload.ticker import Ticker
from EcoFin.options.impliedVolatility import ImpliedVolatility


def main():
    # -------------------------[Set-up]-------------------------
    ticker = Ticker('MSFT')
    optionManager = OptionManager(ticker, now=None)

    i = 0  # <- Time To Maturity curve
    exp = optionManager.getExpirations()[i]

    optionChain = optionManager.getOptionChain(exp=exp)
    # ----------------------------------------------------------

    start_time = time.time()
    impliedVolatility = ImpliedVolatility(optionChain)
    curve = impliedVolatility.getImpliedVolatility()
    print('chrono: {}'.format(time.time() - start_time))

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set(xlabel='Strike', ylabel='Volatility',
           title='Option implied volatility ({})'.format(ticker.getInfo().ticker))

    ax.plot(curve.calls.strike, curve.calls.IV, label='Calls', color='green', alpha=.5)
    ax.plot(curve.puts.strike, curve.puts.IV, label='Puts', color='red', alpha=.5)

    ax.plot(curve.calls.strike, curve.calls.naturalIV, linestyle='dotted', label='Original Calls', color='green')
    ax.plot(curve.puts.strike, curve.puts.naturalIV, linestyle='dotted', label='Original Puts', color='red')

    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
