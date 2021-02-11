"""
functions.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import re

import numpy as np
import pandas as pd
import requests

try:
    import ujson as json
except ImportError:
    import json as json


def emptyDataSerie(index=[]):
    empty = pd.DataFrame(index=index, data={
        'Open': np.nan, 'High': np.nan, 'Low': np.nan,
        'Close': np.nan, 'Adj Close': np.nan, 'Volume': np.nan})
    empty.index.name = 'Date'
    return empty


def parseQuotes(data, tz=None):
    timestamps = data["timestamp"]
    ohlc = data["indicators"]["quote"][0]
    volumes = ohlc["volume"]
    opens = ohlc["open"]
    closes = ohlc["close"]
    lows = ohlc["low"]
    highs = ohlc["high"]

    adjclose = closes
    if "adjclose" in data["indicators"]:
        adjclose = data["indicators"]["adjclose"][0]["adjclose"]

    quotes = pd.DataFrame({"Open": opens,
                           "High": highs,
                           "Low": lows,
                           "Close": closes,
                           "Adj Close": adjclose,
                           "Volume": volumes})

    quotes.index = pd.to_datetime(timestamps, unit="s")
    quotes.sort_index(inplace=True)

    if tz is not None:
        quotes.index = quotes.index.tz_localize(tz)

    return quotes


def camel2title(o):
    return [re.sub("([a-z])([A-Z])", "\g<1> \g<2>", i).title() for i in o]


def getJson(url, proxy=None):
    html = requests.get(url=url, proxies=proxy).text

    if "QuoteSummaryStore" not in html:
        html = requests.get(url=url, proxies=proxy).text
        if "QuoteSummaryStore" not in html:
            return {}

    json_str = html.split('root.App.main =')[1].split(
        '(this)')[0].split(';\n}')[0].strip()
    data = json.loads(json_str)[
        'context']['dispatcher']['stores']['QuoteSummaryStore']

    # return data
    new_data = json.dumps(data).replace('{}', 'null')
    new_data = re.sub(r'\{[\'|\"]raw[\'|\"]:(.*?),(.*?)\}', r'\1', new_data)

    return json.loads(new_data)


def parseEvents(data, tz=None):
    dividends = pd.DataFrame(columns=["Dividends"])
    splits = pd.DataFrame(columns=["Stock Splits"])

    if "events" in data:
        if "dividends" in data["events"]:
            dividends = pd.DataFrame(
                data=list(data["events"]["dividends"].values()))
            dividends.set_index("date", inplace=True)
            dividends.index = pd.to_datetime(dividends.index, unit="s")
            dividends.sort_index(inplace=True)
            if tz is not None:
                dividends.index = dividends.index.tz_localize(tz)

            dividends.columns = ["Dividends"]

        if "splits" in data["events"]:
            splits = pd.DataFrame(
                data=list(data["events"]["splits"].values()))
            splits.set_index("date", inplace=True)
            splits.index = pd.to_datetime(splits.index, unit="s")
            splits.sort_index(inplace=True)
            if tz is not None:
                splits.index = splits.index.tz_localize(tz)
            splits["Stock Splits"] = splits["numerator"] / \
                                     splits["denominator"]
            splits = splits["Stock Splits"]

    return dividends, splits


def autoAdjust(data):
    df = data.copy()
    ratio = df["Close"] / df["Adj Close"]
    df["Adj Open"] = df["Open"] / ratio
    df["Adj High"] = df["High"] / ratio
    df["Adj Low"] = df["Low"] / ratio

    df.drop(
        ["Open", "High", "Low", "Close"],
        axis=1, inplace=True)

    df.rename(columns={
        "Adj Open": "Open", "Adj High": "High",
        "Adj Low": "Low", "Adj Close": "Close"
    }, inplace=True)

    df = df[["Open", "High", "Low", "Close", "Volume"]]
    return df[["Open", "High", "Low", "Close", "Volume"]]


def backAdjust(data):
    """ back-adjusted data to mimic true historical prices """

    df = data.copy()
    ratio = df["Adj Close"] / df["Close"]
    df["Adj Open"] = df["Open"] * ratio
    df["Adj High"] = df["High"] * ratio
    df["Adj Low"] = df["Low"] * ratio

    df.drop(
        ["Open", "High", "Low", "Adj Close"],
        axis=1, inplace=True)

    df.rename(columns={
        "Adj Open": "Open", "Adj High": "High",
        "Adj Low": "Low"
    }, inplace=True)

    return df[["Open", "High", "Low", "Close", "Volume"]]
