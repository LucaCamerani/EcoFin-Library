"""
montecarloSimulation.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import matplotlib.pyplot as plt

from EcoFin.math.stochasticProcess.itoProcess import ItoProcess
from EcoFin.math.stochasticProcess.process import Process

t = 20
T = 100
dt = 1

n = 300

process = Process(T, dt, t=t, n=n)
ito = ItoProcess(T, dt, t=t, x0=100, n=n)

# ---[UNIFORM STOCHASTIC PROCESS]---------------------------------------------
# simulation = process.uniformStochasticProcess()
# ----------------------------------------------------------------------------

# ---[GAUSSIAN STOCHASTIC PROCESS]--------------------------------------------
# simulation = process.gaussianProcess()
# ----------------------------------------------------------------------------

# ---[STANDARD BROWNIAN MOTION]-----------------------------------------------
# simulation = process.standardBrownianMotion().process
# ----------------------------------------------------------------------------

# ============================================================================

# ---[DRIFT BROWNIAN MOTION]--------------------------------------------------
# simulation = ito.driftBrownianMotion(0.1, 0.2)
# ----------------------------------------------------------------------------

# ---[GEOMETRIC BROWNIAN MOTION]----------------------------------------------
simulation = ito.geometricBrownianMotion(0.01, 0.02)
# ----------------------------------------------------------------------------

# ---[GEOMETRIC t-Student MOTION]---------------------------------------------
# simulation = ito.geometricBrownianMotion(0.01, 0.02)
# ----------------------------------------------------------------------------

for i in range(0, n):
    plt.plot(ito.getTimeVector(), simulation[i])
plt.show()
