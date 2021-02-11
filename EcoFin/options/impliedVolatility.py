"""
impliedVolatility.py

Created by Luca Camerani at 18/10/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

from collections import namedtuple

from tqdm import tqdm

from EcoFin.options.blackScholesModel import BSM
from EcoFin.options.optionChain import OptionChain
from EcoFin.stat.interpolation import interpolateNaN


class ImpliedVolatility():
    def __init__(self, optionChain: OptionChain, interpolate=True, progressBar=True, multiprocessing=True):
        self.optionChain = optionChain
        self.r = optionChain.getRiskFreeRate()
        self.interpolate = interpolate
        self.progressBar = progressBar
        self.multiprocessing = multiprocessing
        self.ticker = self.optionChain.getTicker()
        self.underliyngPrice = self.optionChain.getSpotPrice()
        self.chain = self.optionChain.getChain()
        self.date = self.optionChain.getChainDate()
        self.maturity = self.optionChain.getTimeToMaturity()
        self.strikeList = self.optionChain.getStrikeList()
        self.forwardPrice = optionChain.getForwardPrice()

        self.impliedVolatility = self.computeImpliedVolatility()

    def computeImpliedVolatility(self):
        output = {}
        for type, contracts in tqdm({'call': self.chain.calls, 'put': self.chain.puts}.items(),
                                    desc='Compute ImpliedVolatility', disable=not self.progressBar):
            IVs = []
            d2 = []
            for index, contract in contracts.iterrows():
                strike = contract['strike']

                marketPrice = contract['avgPrice']
                option = BSM(self.underliyngPrice, strike, self.r, None, self.maturity.days)

                IV = option.getImpliedVolatility(marketPrice, type)
                IVs.append(IV)

                d2.append(option.computeValues(sigma=IVs[-1]).d2)

            if self.interpolate:
                IVs = interpolateNaN(IVs)
                d2 = interpolateNaN(d2)

            contracts['IV'] = IVs
            contracts['d2'] = d2
            output[type] = contracts.rename(columns={'impliedVolatility': 'naturalIV'})

        return namedtuple('IV', ['calls', 'puts'])(**{
            "calls": output['call'],
            "puts": output['put'],
        })

    def getImpliedVolatility(self):
        return self.impliedVolatility

    def getOptionChain(self):
        return self.optionChain
