"""
ticker.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

from EcoFin.dataDownload.core import TickerCore


class Ticker(TickerCore):
    def __repr__(self):
        return 'EcoFin.Ticker object <%s>' % self.ticker

    @property
    def dividends(self):
        return self.getDividends()

    @property
    def splits(self):
        return self.getSplits()

    @property
    def events(self):
        return self.getEvents()

    @property
    def info(self):
        return self.getInfo()
