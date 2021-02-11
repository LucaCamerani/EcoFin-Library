"""
binomialTree.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""
import numpy as np
from matplotlib import pyplot as plt

from EcoFin.options.binomialTree import OptionTree

# set up tree
tree = OptionTree(30, 29, 40, 0.05, 0.3, N=15, plainVanilla=True, div=0)

# set up plot
fig, axs = plt.subplots(1, 2, figsize=(15, 8), sharey=True, gridspec_kw={'width_ratios': [3, 1]})
fig.suptitle('Sample binomial tree')
fig.tight_layout()

# plot tree
axs[0].set_title('Binomial Tree')
for i in tree.getTimeVector():
    x = [1, 0, 1]
    for j in range(i):
        x.append(0)
        x.append(1)
    x = np.array(x) + i
    y = np.sort(np.append(tree.getUnderlyingAtTime(i), tree.getUnderlyingAtTime(i + 1)))

    axs[0].plot(x, y, 'steelblue')
axs[0].set(xlabel='Time ($t$)', ylabel='Underlying price ($S_t$)')

# plot histogram
axs[1].set_title('Binomial density')
T = tree.getTimeVector()[1]
axs[1].barh(tree.getUnderlyingAtTime(T), tree.getProbabilitiesAtTime(T))
axs[1].set(xlabel='Probabilities')

plt.subplots_adjust(wspace=.001)
plt.show()
