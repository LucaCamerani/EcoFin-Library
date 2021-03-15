"""
shared.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

from EcoFin.dataDownload.cache import Cache

ip = r'http://127.0.0.1:5000/'  # (LOCAL)


def resetUrl():
    global baseUrl, ratesUrl, ratesKEY, poolUrl, ip
    if local_mode is False:
        baseUrl = 'https://query1.finance.yahoo.com'
        ratesUrl = 'https://api.stlouisfed.org/fred/series/observations'
        ratesKEY = 'fe9e3533755ccaa77e92a7d3cb8ef632'
    else:
        baseUrl = '{}/API'.format(ip)
        ratesUrl = '{}/API/finance/rates'.format(ip)
        ratesKEY = None

    poolUrl = '{}/pool'.format(ip)


DFS = {}
PROGRESS_BAR = None
ERRORS = {}

use_cache = True

if "session_cache" not in locals():
    session_cache = Cache()

local_mode = False
show_url = False

resetUrl()


def setIP(IP):
    global ip
    ip = IP

    resetUrl()
