"""
exerciseProbability.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import matplotlib.pyplot as plt
import numpy as np

from EcoFin.options.binomialTree import BinomialTree

prob = {'call': [], 'put': []}
strikes = np.arange(0, 200, 1)

for strike in strikes:
    tree = BinomialTree(100, strike, 50, 0.05, 0.2)
    prob['call'].append(tree.getExerciseProb().call)
    prob['put'].append(tree.getExerciseProb().put)

for type in prob.keys():
    plt.plot(strikes, prob[type], label=type + ' exercise prob')

plt.xlabel('Strike')
plt.ylabel('Probability')
plt.legend()
plt.grid()
plt.show()
