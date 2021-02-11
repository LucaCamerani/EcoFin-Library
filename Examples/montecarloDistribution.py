"""
montecarloDistribution.py

Created by Luca Camerani at 12/09/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import matplotlib.pyplot as plt

from EcoFin.math.stochasticProcess.itoProcess import ItoProcess
from EcoFin.stat.montecarloDistribution import MonteCarlo

t = 20
T = 100
dt = 1

n = 3000
index = 30

ito = ItoProcess(T, dt, t=t, x0=100, n=n)

# ---[GEOMETRIC BROWNIAN MOTION]----------------------------------------------
simulation = ito.geometricBrownianMotion(0.01, 0.02)
# ----------------------------------------------------------------------------

MC = MonteCarlo(simulation)
EPDF = MC.getEmpiricalDist(bandwidth=10, index=index)

plt.hist(MC.getData(index=index), density=True, bins=50, label='Histogram')
plt.plot(EPDF.values, EPDF.probabilities, label='EPDF')
plt.legend()
plt.show()
