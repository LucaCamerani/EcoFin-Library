"""
back_looking.py

Created by Luca Camerani at 27/02/2021, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import seaborn as sns

from tqdm import tqdm

history = 200
visualize = 30

a = np.random.normal(0, 0.5, history)
b = np.random.normal(0, 0.5, history)

for i in tqdm(range(visualize, history)):
    a_s = a[i - visualize:i]
    b_s = b[i - visualize:i]

    # Plot results
    fig, axs = plt.subplots(1, 2, figsize=(5, 2.5), gridspec_kw={'width_ratios': [4, 1]}, sharey=True)

    # 1) Plot driver and quantiles
    axs[0].plot(np.cumsum(a_s), linewidth=3, color='green')
    axs[0].plot(np.cumsum(b_s), linewidth=3, color='red')
    axs[0].axis('off')

    # 2) Plot distribution
    axs[1] = sns.distplot(np.cumsum(a_s), fit=sp.stats.norm, kde=False, hist=False, vertical=True,
                          fit_kws={'color': 'green'})
    axs[1] = sns.distplot(np.cumsum(b_s), fit=sp.stats.norm, kde=False, hist=False, vertical=True,
                          fit_kws={'color': 'red'})

    plt.axis('off')
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.savefig(r'Export\{}.png'.format(i))
