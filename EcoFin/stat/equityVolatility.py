"""
equityVolatility.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import arch
import numpy as np
import pandas as pd


class EquityVolatility:
    def __init__(self, seriesDataFrame, days=260):
        self.days = days
        self.equityData = pd.DataFrame(seriesDataFrame['Close'], columns=["Close"])
        self.equityData["log"] = np.log(self.equityData) - np.log(self.equityData.shift(1))

    def meanSigma(self):
        st = self.equityData["log"].dropna().ewm(span=self.days).std()
        sigma = st.iloc[-1]
        return sigma * np.sqrt(self.days)

    def garchSigma(self):
        model = arch.arch_model(self.equityData["log"].dropna(), mean='Zero', vol='GARCH', p=1, q=1)
        modelFit = model.fit()
        forecast = modelFit.forecast(horizon=1)
        var = forecast.variance.iloc[-1]
        sigma = float(np.sqrt(var))
        return sigma * np.sqrt(self.days)
