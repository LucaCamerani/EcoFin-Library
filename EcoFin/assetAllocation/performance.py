"""
performance.py

Created by Luca Camerani at 06/02/2021, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import math
from collections import namedtuple

import numpy as np
import pandas as pd
from tabulate import tabulate


class ConsoleStyle:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class Performance():
    def __init__(self, benchmark: pd.Series, strategy: pd.Series, days=260, r=0):
        """
        Annualized returns 
        """
        self.days = days
        self.r = r
        self.returns = {'ln': {'benchmark': benchmark,
                               'strategy': strategy},
                        'pct': {'benchmark': np.exp(benchmark) - 1,
                                'strategy': np.exp(strategy) - 1}}
        self.len = benchmark.size
        self.excess = {'ln': benchmark - strategy,
                       'pct': (np.exp(benchmark) - 1) - np.exp(strategy) - 1}

    def getReturn(self):
        return namedtuple('AnnualReturn', ['benchmark', 'strategy'])(**{
            "benchmark": np.exp(self.returns['ln']['benchmark'].sum()) ** (self.days / self.len) - 1,
            "strategy": np.exp(self.returns['ln']['strategy'].sum()) ** (self.days / self.len) - 1
        })

    def getLogReturn(self):
        return namedtuple('AnnualReturn', ['benchmark', 'strategy'])(**{
            "benchmark": self.returns['ln']['benchmark'].sum() / (self.days / self.len),
            "strategy": self.returns['ln']['strategy'].sum() / (self.days / self.len)
        })

    def getExcessReturn(self):
        return namedtuple('ER', ['history', 'value'])(**{
            "history": self.returns['pct']['strategy'] - self.returns['pct']['benchmark'],
            "value": (self.getReturn().strategy - self.getReturn().benchmark)
        })

    def getSharpeRatio(self):
        return namedtuple('SR', ['benchmark', 'strategy'])(**{
            "benchmark": (self.getReturn().benchmark - self.r) /
                         (self.returns['pct']['benchmark'].std() * math.sqrt(self.days)),
            "strategy": (self.getReturn().strategy - self.r) /
                        (self.returns['pct']['strategy'].std() * math.sqrt(self.days))
        })

    def getInformationRatio(self):
        excess = self.getExcessReturn()
        return excess.value / self.getExcessReturn().history.std()

    def getSortinoRatio(self):
        return namedtuple('SO', ['benchmark', 'strategy'])(**{
            "benchmark": (self.getReturn().benchmark - self.r) /
                         (np.std([self.returns['pct']['benchmark'] <= 0]) * math.sqrt(self.days)),
            "strategy": (self.getReturn().strategy - self.r) /
                        (np.std([self.returns['pct']['strategy'] <= 0]) * math.sqrt(self.days))
        })

    def printPerformanceSummary(self):
        a = {'Return (R)': {'Benchmark': "{0:.2%}".format(self.getReturn().benchmark),
                            'Strategy': "{0:.2%}".format(self.getReturn().strategy)},
             'Log-Return (X)': {'Benchmark': "{0:.2f}".format(self.getLogReturn().benchmark),
                                'Strategy': "{0:.2f}".format(self.getLogReturn().strategy)},
             'Sharpe Ratio (SR)': {'Benchmark': "{0:.2f}".format(self.getSharpeRatio().benchmark),
                                   'Strategy': "{0:.2f}".format(self.getSharpeRatio().strategy)},
             'Information Ratio (IR)': {'Benchmark': "{}".format(None),
                                        'Strategy': "{0:.2f}".format(self.getInformationRatio())},
             'Sortino Ratio (SO)': {'Benchmark': "{0:.4f}".format(self.getSortinoRatio().benchmark),
                                    'Strategy': "{0:.4f}".format(self.getSortinoRatio().strategy)}}

        b = {'Sample size': "{}".format(self.len),
             'Annual days': "{}".format(self.days),
             'Risk Free rate': "{0:.2%}".format(self.r)}

        print(ConsoleStyle.BOLD + 'Input summary:' + ConsoleStyle.END)
        print(tabulate(pd.DataFrame.from_dict(b, orient='index'), headers=["Value"], tablefmt="orgtbl"))
        print('\n')
        print(ConsoleStyle.BOLD + 'Strategy performance summary:' + ConsoleStyle.END)
        print(tabulate(pd.DataFrame.from_dict(a, orient='index'), headers="keys", tablefmt="orgtbl"))
