"""
7_synopsis.py

Created by Luca Camerani at 11/12/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

from EcoFin.dataDownload.optionsManager import OptionManager
from EcoFin.dataDownload.ticker import Ticker
from EcoFin.options.chainWeights import ChainWeights
from EcoFin.options.deepOptionChain import DeepOptionChain
from EcoFin.options.optionChainSynopsis import OptionChainSinopsys

# -------------------------[Set-up]-------------------------
ticker = Ticker('MSFT')
optionManager = OptionManager(ticker)
exp = optionManager.getExpirationByMaturity(30, method='greater')
optionChain = optionManager.getOptionChain(exp=exp)
# ----------------------------------------------------------

ticker_info = ticker.getInfo()

deepOptChain = DeepOptionChain(optionChain, True)
chainWeights = ChainWeights(optionChain)

for mode, weights in {'EW': chainWeights.computeEquallyWeights(),
                      'Beta': chainWeights.computeBetaWeights(),
                      'ATM': chainWeights.computeATMWeights(),
                      'OI': chainWeights.computeOpenInterestsWeights(),
                      'Moneyness': chainWeights.computeMoneynessWeights()}.items():
    print('----[{}]----'.format(mode))
    synopsis = OptionChainSinopsys(deepOptChain, weights=weights)

    OPS = synopsis.computeOptionPriceSpread()
    print('OPS:\n • {}\n • {}'.format(OPS.mean, OPS.std))

    IVS = synopsis.computeImpliedVolatilitySpread()
    print('IVS:\n • {}\n • {}'.format(IVS.mean, IVS.std))

    NAP = synopsis.computeNoArbitragePrice()
    print('NAP:\n • {}\n • {}'.format(NAP.value, NAP.ret))

    OIR = synopsis.computeOpenInterestRatio()
    print('OIR:\n • {}\n • {}'.format(OIR.mean, OIR.std))

    PCD = synopsis.computePutCallDelta()
    print('PCD:\n • {}'.format(PCD))
