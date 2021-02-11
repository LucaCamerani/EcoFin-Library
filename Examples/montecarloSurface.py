"""
montecarloSurface.py

Created by Luca Camerani at 13/09/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import matplotlib.pyplot as plt
import numpy as np

from EcoFin.math.stochasticProcess.itoProcess import ItoProcess
from EcoFin.stat.montecarloDistribution import MonteCarlo

t = 20
T = 100
dt = 1

n = 300

ito = ItoProcess(T, dt, t=t, x0=100, n=n)

simulation = None

# ---[GEOMETRIC BROWNIAN MOTION]----------------------------------------------
simulation = ito.geometricBrownianMotion(0.01, 0.02)
# ----------------------------------------------------------------------------

MC = MonteCarlo(simulation)
output = []

for i in MC.getIndexSpace():
    EPDF = MC.getEmpiricalDist(index=i, bandwidth=10, fullSpace=True)
    output.append(EPDF.probabilities)

X, Y = np.meshgrid(MC.getIndexSpace(), MC.getValues())
Z = np.array(output).transpose()

fig = plt.figure(figsize=(15, 8))
ax = fig.add_subplot(111, projection='3d')
fig.suptitle('Montecarlo Distribution Evolution')
surf = ax.plot_surface(X, Y, Z, alpha=.6)

for i in range(0, n):
    plt.plot(MC.getIndexSpace(), simulation[i], alpha=.6)

ax.set_xlabel('Index (time)')
ax.set_ylabel('Value')
ax.set_zlabel('Probability')
plt.show()
