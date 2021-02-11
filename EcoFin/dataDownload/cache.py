"""
cache.py

Created by Luca Camerani at 12/12/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import pickle

from collections import namedtuple
from sys import getsizeof


class Cache():
    def __init__(self, path=None, bytelimit=5000):
        self.bytelimit = bytelimit
        if path is None:
            self.cache = {}
        else:
            with open(path) as f:
                self.cache = pickle.load(f)

    def add(self, key: (str, int), var):
        try:
            self.clearCache()
            self.cache[str(key)] = var
        except Exception as e:
            print(e)
            pass

        return self.cache

    def drop(self, key: (str, int)):
        try:
            del self.cache[key]
        except:
            pass

    def read(self, key: (str, int)):
        try:
            return self.cache[key]
        except:
            return False
            pass

    def keyExists(self, key: (str, int)):
        if key in self.cache.keys():
            return True
        else:
            return False

    def getCache(self):
        return self.cache

    def getCacheSize(self):
        return namedtuple('Size', ['len', 'bytes'])(**{
            "len": len(self.cache),
            "bytes": getsizeof(self.cache)
        })

    def clearCache(self):
        if self.getCacheSize().bytes >= self.bytelimit:
            self.cache = {}

    def storeCache(self, path: str):
        try:
            with open(path, 'w') as f:
                pickle.dump([self.cache], f)
            return True
        except:
            pass
            return False

    def printCache(self):
        summary = self.getCacheSize()
        print('Cache status:\n • Items: {}\n • Bytes: {}'.format(summary.len, summary.bytes))
        print('Data:\n{}'.format([(key, type(self.cache[key])) for key in self.cache.keys()]))
