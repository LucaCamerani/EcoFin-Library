"""
optionChain.py

Created by Luca Camerani at 22/09/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

from collections import namedtuple

import numpy as np
import pandas as pd

from EcoFin.dataDownload.ticker import Ticker
from EcoFin.forward.forward import Forward
from EcoFin.options.utils import daysToMaturity


class OptionChain():
    def __init__(self, ticker: Ticker, chain_data: dict, now: float, expiration: float,
                 underlying_price: float, risk_fee_rate: float):
        self.ticker = ticker
        self.chain_data = chain_data
        self.now = now
        self.exp = expiration
        self.underlying_price = underlying_price
        self.r = risk_fee_rate

    def optionsParse(self, opt):
        data = pd.DataFrame(opt)

        # compute moneyness
        data['moneyness'] = data['strike'] / self.getSpotPrice() - 1

        # compute average Ask/Bid price as best estimate (BEP)
        data['priceQuality'] = 'A'
        data.loc[(data['ask'].isnull()) & (data['bid'].isnull()), ['ask', 'bid', 'priceQuality']] \
            = pd.DataFrame({'ask': data['lastPrice'], 'bid': data['lastPrice'], 'priceQuality': 'C'})
        data.loc[data['ask'].isnull(), ['ask', 'priceQuality']] \
            = pd.DataFrame({'ask': data['bid'], 'priceQuality': 'B_a'})
        data.loc[data['bid'].isnull(), 'bid'] \
            = pd.DataFrame({'bid': data['ask'], 'priceQuality': 'B_b'})
        data['avgPrice'] = (data['ask'] + data['bid']) / 2

        data = data.reindex(columns=[
            'contractSymbol',
            'strike',
            'moneyness',
            'lastTradeDate',
            'bid',
            'ask',
            'avgPrice',
            'lastPrice',
            'priceQuality',
            'volume',
            'openInterest',
            'impliedVolatility',
            'currency'])
        data = data.set_index('contractSymbol')
        data.loc[data['impliedVolatility'] <= 1e-3, 'impliedVolatility'] = np.nan

        data['lastTradeDate'] = pd.to_datetime(
            data['lastTradeDate'], unit='s')

        return data.sort_values(by='strike')

    def getChain(self):
        calls = self.optionsParse(self.chain_data['calls'])
        puts = self.optionsParse(self.chain_data['puts'])
        full = calls.drop(columns=['moneyness', 'currency']). \
            merge(puts, on=['strike'], suffixes=['_call', '_put'])

        return namedtuple('Chain', ['calls', 'puts', 'full'])(**{
            "calls": calls,
            "puts": puts,
            "full": full
        })

    def getTimeToMaturity(self):
        days = daysToMaturity(self.getChainExpiration(), fromDate=self.getChainDate())
        return namedtuple('Maturity', ['days', 'years'])(**{
            "days": days,
            "years": days / float(365)
        })

    def getRiskFreeRate(self):
        return self.r

    def getSpotPrice(self):
        return self.underlying_price

    def getForwardPrice(self):
        forward = Forward(self.getSpotPrice(), self.getRiskFreeRate(), self.getTimeToMaturity().days)

        return forward.getForwardPrice()

    def getChainExpiration(self):
        return self.exp

    def getChainDate(self):
        return self.now

    def getStrikeList(self):
        return list(self.getChain().full.strike)

    def getTicker(self):
        return self.ticker

    def getSummary(self):
        return {'Ticker': self.getTicker().ticker,
                'Now': self.getChainDate(),
                'Exp': self.getChainExpiration(),
                'S': self.getSpotPrice(),
                'F': self.getForwardPrice(),
                'r': self.getRiskFreeRate(),
                'TimeToMaturity': self.getTimeToMaturity()
                }
