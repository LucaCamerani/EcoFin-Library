"""
deepOptionChain.py

Created by Luca Camerani at 15/11/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import numpy as np

from EcoFin.options.blackScholesModel import BSM
from EcoFin.options.binomialTree import BinomialTree
from EcoFin.options.impliedVolatility import ImpliedVolatility
from EcoFin.options.optionChain import OptionChain
from EcoFin.options.volatilitySmile import VolatilitySmile
from EcoFin.stat.equityVolatility import EquityVolatility
from EcoFin.stat.interpolation import interpolateNaN


class DeepOptionChain():
    def __init__(self, optionChain: OptionChain, computeIV: bool = True, computeBSM=True, progressBar=True):
        self.optionChain = optionChain
        self.progressbar = progressBar
        self.computeIV = computeIV
        self.computeBSM = computeBSM

        self.deepOptionChain = self.computeDeepOptionChain()

    def computeDeepOptionChain(self):
        ticker = self.optionChain.getTicker()
        series = ticker.getHistory(period="1y", interval="1d")
        price = self.optionChain.getSpotPrice()

        r = self.optionChain.getRiskFreeRate()
        sigma = EquityVolatility(series).meanSigma()
        maturity = self.optionChain.getTimeToMaturity()

        chain = self.optionChain.getChain()

        # compute theoretical prices
        data = chain.full.copy()
        if self.computeBSM:
            data['TheoPrice_call'] = None
            data['TheoPrice_put'] = None
            for strike in data.strike:
                if self.optionChain.isPlainVanilla():   # PlainVanilla
                    option = BSM(price, strike, r, sigma, maturity.days)
                    optPrice = option.computePrice()
                else:                                   # American exercise
                    option = BinomialTree(price, strike, maturity.days, r, sigma, N=80, plainVanilla=False)
                    optPrice = option.computePrice()

                data.loc[data.strike == strike, ['TheoPrice_call', 'TheoPrice_put']] = [optPrice.call, optPrice.put]

            data['avgPrice_call'] = interpolateNaN(data.avgPrice_call)
            data['avgPrice_put'] = interpolateNaN(data.avgPrice_put)
            data['spread_call'] = data['avgPrice_call'] - data['TheoPrice_call']
            data['spread_put'] = data['avgPrice_put'] - data['TheoPrice_put']
            data['spreadSummary'] = data['spread_call'] - data['spread_put']
        else:
            data['spreadSummary'] = data['avgPrice_call'] - data['avgPrice_put'] - \
                                    (self.optionChain.getSpotPrice() - data['strike'] *
                                     np.exp(-self.optionChain.getRiskFreeRate() * self.optionChain.getTimeToMaturity().years))

        if self.computeIV:
            # compute IVs and IV spread
            impliedVolatility = ImpliedVolatility(self.optionChain, True, self.progressbar)
            IVs = impliedVolatility.getImpliedVolatility()
            data = data.merge(IVs.calls[['strike', 'IV', 'd2']], on=['strike'], how='left')
            data = data.merge(IVs.puts[['strike', 'IV', 'd2']], on=['strike'], how='left', suffixes=['_call', '_put'])
            data['IV_spread'] = data['IV_call'] - data['IV_put']

            # compute volatility smile
            self.volatilitysmile = VolatilitySmile(impliedVolatility)
            smile = self.volatilitysmile.getVolatilitySmile()
            data = data.merge(smile[['strike', 'smile', 'naturalSmile', 'avgPrice']], on=['strike'], how='left')
        else:
            F = self.optionChain.getForwardPrice()
            data.loc[data.strike >= F, 'avgPrice'] = data['avgPrice_call']
            data.loc[data.strike < F, 'avgPrice'] = data['avgPrice_put']

        # compute no-arbitrage bounds
        div = 0
        data['S_U'] = data['ask_call'] + data['strike'] + div - data['bid_put']
        data['S_L'] = data['bid_call'] + data['strike'] * np.exp(-r * maturity.years) - data['ask_put']

        # compute Open Interest Ratio
        data['openInterestRatio'] = ((data['openInterest_call'] / (
                    data['openInterest_put'] + data['openInterest_call'])).
                                     replace({np.inf: 0, np.nan: 0}) - 0.5) * 2

        # compute price delta
        data['PutCallDelta'] = (data['avgPrice_call'] - data['avgPrice_put']).abs()

        return data

    def getDeepOptionChain(self):
        return self.deepOptionChain

    def getOptionChain(self):
        return self.optionChain

    def getVolatilitySmile(self):
        return self.volatilitysmile
