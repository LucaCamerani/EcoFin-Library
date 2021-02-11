"""
rates.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import json
import urllib.request

import numpy as np
import pandas as pd

from EcoFin.dataDownload import shared


class Rates():
    def __init__(self):
        self.url = shared.ratesUrl
        self.key = shared.ratesKEY

    def download_series(self, ticker: str):
        url = "{}?series_id={}&api_key={}&file_type=json".format(self.url, ticker, self.key)

        if shared.show_url: print('Connection request: {}'.format(url))

        if shared.use_cache & shared.session_cache.keyExists(url):
            data = shared.session_cache.read(url)
        else:
            with urllib.request.urlopen(url) as urll:
                data = json.loads(urll.read().decode())
            shared.session_cache.add(key=url, var=data)

        series = pd.DataFrame(data['observations']).set_index('date')['value']

        try:
            series = series.replace({'.': np.nan}).astype(float)
        except:
            pass
        series.index = pd.to_datetime(series.index)

        return series

    def getCurrent(self, code="DTB3"):
        return self.getHistory(code)[-1]

    def getHistory(self, code="DTB3"):
        # DGS3MO <-- LIBOR
        data = self.download_series('DTB3')
        output = (data / float(100)).interpolate()

        return output
