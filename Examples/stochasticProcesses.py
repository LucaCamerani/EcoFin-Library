"""
process.py

Created by Luca Camerani at 03/09/2020, University of Milano-Bicocca.
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

process = Process(T, dt, t=t)
ito = ItoProcess(T, dt, t=t, x0=100)

# ---[UNIFORM STOCHASTIC PROCESS]---------------------------------------------
"""
plt.plot(process.getTimeVector(), process.uniformStochasticProcess())
plt.show()
"""
# ----------------------------------------------------------------------------

# ---[GAUSSIAN STOCHASTIC PROCESS]--------------------------------------------
"""
plt.plot(process.getTimeVector(), process.gaussianProcess())
plt.show()
"""
# ----------------------------------------------------------------------------

# ---[STANDARD BROWNIAN MOTION]-----------------------------------------------
"""
plt.plot(process.getTimeVector(), process.standardBrownianMotion().process)
plt.show()
"""
# ----------------------------------------------------------------------------

# ============================================================================

# ---[DRIFT BROWNIAN MOTION]--------------------------------------------------

plt.plot(ito.getTimeVector(), ito.driftBrownianMotion(0.1, 0.2))
plt.show()

# ----------------------------------------------------------------------------

# ---[GEOMETRIC BROWNIAN MOTION]----------------------------------------------
"""
plt.plot(ito.getTimeVector(), ito.geometricBrownianMotion(0.01, 0.02))
plt.show()
"""
# ----------------------------------------------------------------------------
