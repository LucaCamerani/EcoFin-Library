"""
blackScholesPrice.py

Created by Luca Camerani at 31/08/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import matplotlib.pyplot as plt

from EcoFin.options.blackScholesModel import BSM

prices = {'call': [], 'put': []}
strikes = range(1, 200, 5)

for strike in strikes:
    option = BSM(100, strike, 0.05, 0.2, 365)
    price = option.computePrice()
    prices['call'].append(price.call)
    prices['put'].append(price.put)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
fig.suptitle('Sample option price')

ax1.set_title('Call')
ax1.plot(strikes, prices['call'], color='green', label='Call option')
ax1.set(xlabel='Strike')
ax1.set(ylabel='Price')
ax1.legend()

ax2.set_title('Put')
ax2.plot(strikes, prices['put'], color='red', label='Put option')
ax2.set(xlabel='Strike')
ax2.set(ylabel='Price')
ax2.legend()

plt.show()
