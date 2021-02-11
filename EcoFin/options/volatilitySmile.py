"""
volatilitySmile.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import pandas as pd

from EcoFin.options.impliedVolatility import ImpliedVolatility


class VolatilitySmile():
    def __init__(self, impliedVolatility: ImpliedVolatility, interpolate=True):
        self.optionChain = impliedVolatility.getOptionChain()
        self.r = self.optionChain.getRiskFreeRate()
        self.interpolate = interpolate
        self.ticker = self.optionChain.getTicker()
        self.underliyngPrice = self.optionChain.getSpotPrice()
        self.chain = self.optionChain.getChain()
        self.date = self.optionChain.getChainDate()
        self.maturity = self.optionChain.getTimeToMaturity()
        self.strikeList = self.optionChain.getStrikeList()
        self.forwardPrice = self.optionChain.getForwardPrice()

        self.impliedVolatility = impliedVolatility
        self.volatilitySmile = self.computeVolatilitySmile()

    def computeVolatilitySmile(self):
        skew = self.impliedVolatility.getImpliedVolatility()

        output = []

        contracts = skew.calls
        mask = contracts.strike >= self.forwardPrice
        output.append(contracts[mask])

        contracts = skew.puts
        mask = contracts.strike < self.forwardPrice
        output.append(contracts[mask])

        output = pd.concat(output, ignore_index=True)
        output.rename(columns={'IV': 'smile', 'naturalIV': 'naturalSmile'}, inplace=True)

        return output.sort_values(by=['strike'])

    def getVolatilitySmile(self):
        return self.volatilitySmile

    def getImpliedVolatility(self):
        return self.impliedVolatility

    def getOptionChain(self):
        return self.optionChain
