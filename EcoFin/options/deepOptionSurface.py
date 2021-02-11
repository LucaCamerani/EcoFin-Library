"""
deepOptionSurface.py

Created by Luca Camerani at 11/12/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

from tqdm import tqdm

from EcoFin.options.deepOptionChain import DeepOptionChain
from EcoFin.options.optionSurface import OptionSurface


class DeepOptionSurface():
    def __init__(self, optionSurface: OptionSurface, computeIV: bool = True, computeBSM=True, progressBar=True):
        self.progressBar = progressBar
        self.optionSurface = optionSurface
        self.computeIV = computeIV
        self.computeBSM = computeBSM

        self.surface_data = self.computeDeepOptionSurface()

    def computeDeepOptionSurface(self):
        deep_data = {}
        for expiration in tqdm(self.optionSurface.getExpirations(), desc='Compute IV surface',
                               disable=not self.progressBar):
            chain = self.getOptionSurface().getChainByDate(expiration)
            deep_data[expiration] = DeepOptionChain(chain, computeIV=self.computeIV, computeBSM=self.computeBSM,
                                                    progressBar=False)

        return deep_data

    def getDeepChainByDate(self, date: (str, int)):
        return self.surface_data[int(date)]

    def getDeepChainByIndex(self, index: int):
        return self.surface_data[self.getOptionSurface().getExpirations()[index]]

    def getDeepChainByMaturity(self, maturity_days: (int, float)):
        target = self.getOptionSurface().now + maturity_days * 86400
        chain = self.surface_data[int(self.getNearestExpiration(target))]

        return chain

    def getDeepSurfaceData(self):
        return self.surface_data

    def getOptionSurface(self):
        return self.optionSurface

    def getNearestExpiration(self, date: (int, float)):
        return min(self.getOptionSurface().getExpirations(), key=lambda x: abs(x - date))
