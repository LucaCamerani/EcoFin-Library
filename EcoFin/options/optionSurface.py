"""
optionSurface.py

Created by Luca Camerani at 11/12/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

from EcoFin.dataDownload.ticker import Ticker


class OptionSurface():
    def __init__(self, ticker: Ticker, surface_data: dict, now: float, underlying_price: float, risk_fee_rate: float):
        self.ticker = ticker
        self.surface_data = surface_data
        self.now = now
        self.underlying_price = underlying_price
        self.r = risk_fee_rate

    def getChainByDate(self, date: (str, int)):
        return self.surface_data[int(date)]

    def getChainByIndex(self, index: int):
        return self.surface_data[self.getExpirations()[index]]

    def getChainByMaturity(self, maturity_days: (int, float), method='nearest'):
        target = self.now + maturity_days * 86400
        chain = self.surface_data[int(self.getNearestExpiration(target))]

        return chain

    def getRiskFreeRate(self):
        return self.r

    def getSpotPrice(self):
        return self.underlying_price

    def getDate(self):
        return self.now

    def getStrikeList(self):
        return None

    def getTicker(self):
        return self.ticker

    def getExpirations(self):
        return list(self.surface_data.keys())

    def countChains(self):
        return len(self.surface_data.keys())

    def getNearestExpiration(self, date: (int, float)):
        return min(self.getExpirations(), key=lambda x: abs(x - date))
