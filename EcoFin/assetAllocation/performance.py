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
from tabulate import tabulate
from EcoFin.utils.utils import *


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
    def __init__(self, benchmark: pd.Series, strategy: (pd.Series, dict), days=260, r=0):
        """
        Annualized returns 
        """
        # check for multiple strategies
        strategy = expandToDictionary(strategy, 'Strategy')

        self.days = days
        self.r = r
        self.returns = {'ln': {'benchmark': benchmark,
                               'strategy': strategy},
                        'pct': {'benchmark': np.exp(benchmark) - 1,
                                'strategy': {key: np.exp(data) - 1 for key, data in strategy.items()}}}
        self.len = benchmark.size

        self.excess = {'ln': {key: benchmark - data for key, data in strategy.items()},
                       'pct': {key: (np.exp(benchmark) - 1) - (np.exp(data) - 1) for key, data in strategy.items()}}

    def getReturn(self):
        strategy = reduceDictionary({key: np.exp(data.sum()) ** (self.days / self.len) - 1
                                     for key, data in self.returns['ln']['strategy'].items()})

        return namedtuple('AnnualReturn', ['benchmark', 'strategy'])(**{
            "benchmark": np.exp(self.returns['ln']['benchmark'].sum()) ** (self.days / self.len) - 1,
            "strategy": strategy
        })

    def getLogReturn(self):
        strategy = reduceDictionary({key: data.sum() / (self.days / self.len)
                                     for key, data in self.returns['ln']['strategy'].items()})

        return namedtuple('AnnualReturn', ['benchmark', 'strategy'])(**{
            "benchmark": self.returns['ln']['benchmark'].sum() / (self.days / self.len),
            "strategy": strategy
        })

    def getExcessReturn(self):
        history = reduceDictionary({key: data - self.returns['pct']['benchmark']
                                    for key, data in self.returns['pct']['strategy'].items()})
        value = reduceDictionary({key: data - self.getReturn().benchmark
                                  for key, data in expandToDictionary(self.getReturn().strategy, 'Strategy').items()})

        return namedtuple('ER', ['history', 'value'])(**{
            "history": history,
            "value": value
        })

    def getSharpeRatio(self):
        strategy = reduceDictionary({key: (expandToDictionary(self.getReturn().strategy, 'Strategy')[key] - self.r) /
                                          (self.returns['pct']['strategy'][key].std() * math.sqrt(self.days))
                                     for key in self.returns['pct']['strategy'].keys()})

        return namedtuple('SR', ['benchmark', 'strategy'])(**{
            "benchmark": (self.getReturn().benchmark - self.r) /
                         (self.returns['pct']['benchmark'].std() * math.sqrt(self.days)),
            "strategy": strategy
        })

    def getInformationRatio(self):
        excess = expandToDictionary(self.getExcessReturn(), 'Strategy')
        output = reduceDictionary({key: excess[key].value / expandToDictionary(self.getExcessReturn().history, 'Strategy')[key].std()
                                   for key in expandToDictionary(self.returns['pct']['strategy'], 'Strategy').keys()})

        return output

    def getSortinoRatio(self):
        strategy = reduceDictionary({key: (expandToDictionary(self.getReturn().strategy, 'Strategy')[key] - self.r) /
                                          (np.std([self.returns['pct']['strategy'][key] <= 0]) * math.sqrt(self.days))
                                     for key in expandToDictionary(self.returns['pct']['strategy'], 'Strategy').keys()})

        return namedtuple('SO', ['benchmark', 'strategy'])(**{
            "benchmark": (self.getReturn().benchmark - self.r) /
                         (np.std([self.returns['pct']['benchmark'] <= 0]) * math.sqrt(self.days)),
            "strategy": strategy
        })

    def printPerformanceSummary(self):
        a = {'Return (R)': mergeDict({'Benchmark': "{0:.2%}".format(self.getReturn().benchmark)},
                                     {key: "{0:.2%}".format(data)
                                      for key, data in
                                      expandToDictionary(self.getReturn().strategy, 'Strategy').items()}),
             'Log-Return (X)': mergeDict({'Benchmark': "{0:.2f}".format(self.getLogReturn().benchmark)},
                                         {key: "{0:.2f}".format(data)
                                          for key, data in
                                          expandToDictionary(self.getLogReturn().strategy, 'Strategy').items()}),
             'Sharpe Ratio (SR)': mergeDict({'Benchmark': "{0:.2f}".format(self.getSharpeRatio().benchmark)},
                                            {key: "{0:.2f}".format(data)
                                            for key, data in
                                            expandToDictionary(self.getSharpeRatio().strategy, 'Strategy').items()}),
             'Information Ratio (IR)': mergeDict({'Benchmark': "{}".format(None)},
                                     {key: "{0:.2f}".format(data)
                                      for key, data in
                                      expandToDictionary(self.getInformationRatio(), 'Strategy').items()}),
             'Sortino Ratio (SO)': mergeDict({'Benchmark': "{0:.4f}".format(self.getSortinoRatio().benchmark)},
                                     {key: "{0:.4f}".format(data)
                                      for key, data in
                                      expandToDictionary(self.getSortinoRatio().strategy, 'Strategy').items()})
             }

        b = {'Sample size': "{}".format(self.len),
             'Annual days': "{}".format(self.days),
             'Risk Free rate': "{0:.2%}".format(self.r)}

        print(ConsoleStyle.BOLD + 'Input summary:' + ConsoleStyle.END)
        print(tabulate(pd.DataFrame.from_dict(b, orient='index'), headers=["Value"], tablefmt="orgtbl"))
        print('\n')
        print(ConsoleStyle.BOLD + 'Strategy performance summary:' + ConsoleStyle.END)
        print(tabulate(pd.DataFrame.from_dict(a, orient='index'), headers="keys", tablefmt="orgtbl"))
