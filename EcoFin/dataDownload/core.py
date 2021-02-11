"""
core.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

from collections import namedtuple

import numpy as np
import pandas as pd
import requests

from EcoFin.dataDownload import functions as fc
from EcoFin.dataDownload import shared

try:
    from urllib.parse import quote as urlencode
except ImportError:
    from urllib import quote as urlencode


class TickerCore():
    def __init__(self, ticker):
        self.ticker = ticker.upper()
        self.history = None
        self.baseUrl = shared.baseUrl

        self.fundamentals = False
        self._info = None
        self._sustainability = None
        self._recommendations = None
        self._majorHolders = None
        self._institutionalHolders = None
        self._ISIN = None

        self._calendar = None
        self._expirations = {}

        self._earnings = {
            "Y": fc.emptyDataSerie(),
            "Q": fc.emptyDataSerie()}
        self._financials = {
            "Y": fc.emptyDataSerie(),
            "Q": fc.emptyDataSerie()}
        self._balancesheet = {
            "Y": fc.emptyDataSerie(),
            "Q": fc.emptyDataSerie()}
        self._cashflow = {
            "Y": fc.emptyDataSerie(),
            "Q": fc.emptyDataSerie()}

    def getHistory(self, interval="1d",
                   start=None, end=None, actions=True,
                   autoAdjust=True, backAdjust=False,
                   proxy=None, rounding=True, **kwargs):
        """
        :Parameters:
            period : str
                Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                Either Use period parameter or use start and end
            interval : str
                Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                Intraday data cannot extend last 60 days
            start: str
                Download start date string (YYYY-MM-DD) or datetime.
                Default is 1900-01-01
            end: str
                Download end date string (YYYY-MM-DD) or datetime.
                Default is now
            prepost : bool
                Include Pre and Post market data in results?
                Default is False
            autoAdjust: bool
                Adjust all OHLC automatically? Default is True
            backAdjust: bool
                Back-adjusted data to mimic true historical prices
            proxy: str
                Optional. Proxy server URL scheme. Default is None
            rounding: bool
                Round values to 2 decimal places?
                Optional. Default is False = precision suggested by Yahoo!
            tz: str
                Optional timezone locale for dates.
                (default data is returned as non-localized dates)
            **kwargs: dict
                debug: bool
                    Optional. If passed as False, will suppress
                    error message printing to console.
        """
        params = {"period1": start, "period2": end}
        params["events"] = "div,splits"

        # setup proxy in requests format
        if proxy is not None:
            if isinstance(proxy, dict) and "https" in proxy:
                proxy = proxy["https"]
            proxy = {"https": proxy}

        # Getting data from json
        url = "{}/v8/finance/chart/{}".format(self.baseUrl, self.ticker)
        key = '{}?{}'.format(url, '&'.join(['{}={}'.format(k, d) for k, d in params.items()]))
        if shared.show_url: print('Connection request: {}'.format(key))

        if shared.use_cache & shared.session_cache.keyExists(key):
            data = shared.session_cache.read(key)
        else:
            data = requests.get(url=url, params=params, proxies=proxy)
            if "Server" in data.text:
                raise RuntimeError("Data provider is currently down!")
            data = data.json()
            shared.session_cache.add(key=key, var=data)

        # Clean up errors
        debug_mode = True
        if "debug" in kwargs and isinstance(kwargs["debug"], bool):
            debug_mode = kwargs["debug"]

        err_msg = "No data found for this date range"
        if "chart" in data and data["chart"]["error"]:
            err_msg = data["chart"]["error"]["description"]
            shared.DFS[self.ticker] = fc.emptyDataSerie()
            shared.ERRORS[self.ticker] = err_msg
            if "many" not in kwargs and debug_mode:
                print('- %s: %s' % (self.ticker, err_msg))

            return shared.DFS[self.ticker]

        elif "chart" not in data or data["chart"]["result"] is None or not data["chart"]["result"]:
            shared.DFS[self.ticker] = fc.emptyDataSerie()
            shared.ERRORS[self.ticker] = err_msg
            if "many" not in kwargs and debug_mode:
                print('- %s: %s' % (self.ticker, err_msg))

            return shared.DFS[self.ticker]

        # parse quotes
        try:
            quotes = fc.parseQuotes(data["chart"]["result"][0])
        except Exception:
            shared.DFS[self.ticker] = fc.emptyDataSerie()
            shared.ERRORS[self.ticker] = err_msg
            if "many" not in kwargs and debug_mode:
                print('- %s: %s' % (self.ticker, err_msg))
            return shared.DFS[self.ticker]

        # 2) fix weired bug with Yahoo! - returning 60m for 30m bars
        if interval.lower() == "30m":
            quotes2 = quotes.resample('30T')
            quotes = pd.DataFrame(index=quotes2.last().index, data={
                'Open': quotes2['Open'].first(),
                'High': quotes2['High'].max(),
                'Low': quotes2['Low'].min(),
                'Close': quotes2['Close'].last(),
                'Adj Close': quotes2['Adj Close'].last(),
                'Volume': quotes2['Volume'].sum()
            })
            try:
                quotes['Dividends'] = quotes2['Dividends'].max()
            except Exception:
                pass
            try:
                quotes['Stock Splits'] = quotes2['Dividends'].max()
            except Exception:
                pass

        if autoAdjust:
            quotes = fc.autoAdjust(quotes)
        elif backAdjust:
            quotes = fc.backAdjust(quotes)

        if rounding:
            quotes = np.round(quotes, data["chart"]["result"][0]["meta"]["priceHint"])
        quotes['Volume'] = quotes['Volume'].fillna(0).astype(np.int64)

        quotes.dropna(inplace=True)

        # actions
        dividends, splits = fc.parseEvents(data["chart"]["result"][0])

        # combine
        df = pd.concat([quotes, dividends, splits], axis=1, sort=True)
        df["Dividends"].fillna(0, inplace=True)
        df["Stock Splits"].fillna(0, inplace=True)

        # index eod/intraday
        df.index = df.index.tz_localize("UTC").tz_convert(
            data["chart"]["result"][0]["meta"]["exchangeTimezoneName"])
        df.index = pd.to_datetime(df.index.date)
        df.index.name = "Date"

        self.history = df.copy()

        if not actions:
            df.drop(columns=["Dividends", "Stock Splits"], inplace=True)

        return df.drop_duplicates()

    def getDividends(self, proxy=None):
        if self.history is None:
            self.getHistory(period="max", proxy=proxy)
        dividends = self.history["Dividends"]

        return dividends[dividends != 0]

    def getSplits(self, proxy=None):
        if self.history is None:
            self.getHistory(period="max", proxy=proxy)
        splits = self.history["Stock Splits"]

        return splits[splits != 0]

    def getEvents(self, proxy=None):
        if self.history is None:
            self.getHistory(period="max", proxy=proxy)
        actions = self.history[["Dividends", "Stock Splits"]]

        return actions[actions != 0].dropna(how='all').fillna(0)

    def getInfo(self):
        url = "{}/quote/{}".format(self.baseUrl, self.ticker)
        if shared.show_url: print('Connection request: {}'.format(url))

        try:
            if shared.use_cache & shared.session_cache.keyExists(url):
                data = shared.session_cache.read(url)
            else:
                data = requests.get(url=url)
                if "Server" in data.text:
                    raise RuntimeError("Data provider is currently down!")

                data = data.json()
                shared.session_cache.add(key=url, var=data)

        except:
            data = {"index": 0,
                    "Ticker": None,
                    "ISIN": None,
                    "Long_Name": None,
                    "Website": None,
                    "Region": None,
                    "Quote_Type": None,
                    "Currency": None,
                    "Exchange": None}

        return namedtuple('Info', ['ticker', 'ISIN', 'longName',
                                   'website', 'region', 'quoteType',
                                   'currency', 'exchange'])(**{
            "ticker": data['Ticker'],
            "ISIN": data['ISIN'],
            "longName": data['Long_Name'],
            "website": data['Website'],
            "region": data['Region'],
            "quoteType": data['Quote_Type'],
            "currency": data['Currency'],
            "exchange": data['Exchange']
        })
