"""
optionsManager.py

Created by Luca Camerani at 08/12/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import requests

from EcoFin.dataDownload import shared
from EcoFin.dataDownload.rates import Rates
from EcoFin.dataDownload.ticker import Ticker
from EcoFin.options.optionChain import OptionChain
from EcoFin.options.optionSurface import OptionSurface
from EcoFin.utils.utils import *


class OptionManager():
    def __init__(self, ticker: Ticker, now: int = None):
        self.baseUrl = shared.baseUrl
        self.ticker = ticker
        self.ticker_name = ticker.ticker
        self.setNow(now)

    def checkNow(self):
        if self.downloadOptionChain():
            return True
        else:
            return False

    def downloadOptionChain(self, exp: int=None):
        """
        Note: now and exp in unixtimestamp format!
        """
        try:
            if exp is None and self.now is None:
                url = "{}/v7/finance/options/{}".format(
                    self.baseUrl, self.ticker_name)
            elif exp is not None and self.now is None:
                url = "{}/v7/finance/options/{}?date={}".format(
                    self.baseUrl, self.ticker_name, exp)
            elif exp is None and self.now is not None:
                url = "{}/v7/finance/options/{}?now={}".format(
                    self.baseUrl, self.ticker_name, self.now)
            else:
                url = "{}/v7/finance/options/{}?now={}&date={}".format(
                    self.baseUrl, self.ticker_name, self.now, exp)
            if shared.show_url: print('Connection request: {}'.format(url))

            rateHistory = Rates().getHistory()

            if shared.use_cache & shared.session_cache.keyExists(url):
                r = shared.session_cache.read(url)
            else:
                r = requests.get(url=url).json()
                shared.session_cache.add(key=url, var=r)

            if r['optionChain']['result']:
                r['optionChain']['result'][0]['options'][0]['underlying'] = r['optionChain']['result'][0]['quote']
                r['optionChain']['result'][0]['options'][0]['expirations'] = r['optionChain']['result'][0][
                    'expirationDates']

                try:
                    r['optionChain']['result'][0]['options'][0]['now'] = r['optionChain']['result'][0]['now']
                except:
                    r['optionChain']['result'][0]['options'][0]['now'] = datetime.utcnow().timestamp()

                rate = rateHistory.iloc[rateHistory.index.get_loc(
                    unixtimestamp_to_date(r['optionChain']['result'][0]['options'][0]['now']),
                    method='nearest')]
                r['optionChain']['result'][0]['options'][0]['riskFreeRate'] = rate

                return r['optionChain']['result'][0]['options'][0]
        except:
            return False

    def getNow(self):
        if self.now is None:
            self.now = self.downloadOptionChain()['now']

        return self.now

    def getExpirations(self):
        """
        Returns a list containing expirations at date for ticker.
        If now is none, returns last available data.
        """
        exp_list = sorted(self.downloadOptionChain()['expirations'])

        return exp_list

    def getOptionChain(self, exp: int = None):
        """
        Returns an OptionChain object.
        Note: if option chain doesn't exists returns False
        """
        data = self.downloadOptionChain(exp=exp)

        if data != False:
            exp = data['expirationDate']
            now = data['now']
            price = data['underlying']['regularMarketPrice']
            rf = data['riskFreeRate']

            option_chain = OptionChain(self.ticker, data, now, exp, price, rf)
        else:
            option_chain = False

        return option_chain

    def getOptionSurface(self):
        """
        Returns an oprionSurface object that contains option chains (one for each expiration date) at now date.
        """
        data = {}
        for expiration in self.getExpirations():
            chain = self.getOptionChain(exp=expiration)
            data[expiration] = chain

            now = chain.getChainDate()
            price = chain.getSpotPrice()
            rf = chain.getRiskFreeRate()

        optionSurface = OptionSurface(self.ticker, data, now, price, rf)

        return optionSurface

    def setNow(self, now: int = None):
        """
        Set-up new now date
        """
        self.now = now
        if self.checkNow():
            return self.now
        else:
            return False

    def getExpirationByMaturity(self, maturity_days: (int, float), method='nearest'):
        """
        Returns the nearest expiration by setting a date. If not specified it returns the first expiration.
        Methods:
            * absolute -> absoute nearest;
            * greater -> >=;
            * less -> <=.
        """
        target = self.getNow() + maturity_days * 86400

        return self.getNearestExpiration(target, method)

    def getNearestExpiration(self, date: (int, float) = 0, method='nearest'):
        """
        Returns the nearest expiration by setting a date. If not specified it returns the first expiration.
        Methods:
            * absolute -> absoute nearest;
            * greater -> >=;
            * less -> <=.
        """
        exps = self.getExpirations()
        date = int(date)

        if method is 'nearest':
            return min(exps, key=lambda x: abs(x - date))
        elif method is 'greater':
            return min([i for i in exps if i >= date], key=lambda x: abs(x - date))
        elif method is 'less':
            return min([i for i in exps if i <= date], key=lambda x: abs(x - date))
        else:
            print('Invalid method: {}'.format(method))
