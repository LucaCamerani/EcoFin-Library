"""
1_historyBuilder.py

Created by Luca Camerani at 12/12/2020, University of Milano-Bicocca.
(l.camerani@campus.unimib.it)
All rights reserved.

This file is part of the EcoFin-Library (https://github.com/LucaCamerani/EcoFin-Library),
and is released under the "BSD Open Source License".
"""

import datetime
import os
from multiprocessing import Pool

from tqdm import tqdm

from EcoFin.dataDownload.optionsManager import OptionManager
from EcoFin.dataDownload.shared import *
from EcoFin.dataDownload.ticker import Ticker
from EcoFin.options.chainWeights import ChainWeights
from EcoFin.options.deepOptionChain import DeepOptionChain
from EcoFin.options.equityVIX import EquityVIX
from EcoFin.options.optionChainSynopsis import OptionChainSinopsys
from EcoFin.utils.utils import *

# -------------------------[Set-up]-------------------------
setIP(r'http://127.0.0.1:5000/')
ticker_list = [line.rstrip('\n') for line in open(r'../INDEXs/DJIA.txt')]

multiprocess = True  # use Pool multiprocess system
increment = 86400  # 1 day
maturity_min = 20  # days
computeIV = True  # False for time saving mode
logs = []

# 5Y
date1 = 1420070400
date2 = 1577664000
# Custom
"""
date1 = 1551657600 # Monday 4 March 2019
date2 = date1 + increment * 7
"""


# ----------------------------------------------------------

def execute(tick: str):
    ticker = Ticker(tick)
    optionManager = OptionManager(ticker)

    output = pd.DataFrame
    for now in range(date1, date2, increment):  # Compute day by day
        try:
            # Exclude bad results and weekends
            if optionManager.setNow(now) is not False and datetime.fromtimestamp(now).weekday() not in [5, 6]:
                exp = optionManager.getExpirationByMaturity(maturity_min, method='greater')
                optionChain = optionManager.getOptionChain(exp=exp)
                deepOptionChain = DeepOptionChain(optionChain, computeIV=computeIV, progressBar=False)

                summary = {'Date': unixtimestamp_to_date(optionChain.getChainDate()),
                           'Exp': unixtimestamp_to_date(optionChain.getChainExpiration()),
                           'Maturity': optionChain.getTimeToMaturity().days,
                           'ForwardPrice': optionChain.getForwardPrice(),
                           'SpotPrice': optionChain.getSpotPrice(),
                           }

                # compute signals
                chainWeights = ChainWeights(optionChain)
                for mode, weights in {'EW': chainWeights.computeEquallyWeights(),
                                      'Beta': chainWeights.computeBetaWeights(),
                                      'ATM': chainWeights.computeATMWeights(),
                                      'OI': chainWeights.computeOpenInterestsWeights(),
                                      'Moneyness': chainWeights.computeMoneynessWeights()}.items():
                    synopsis = OptionChainSinopsys(deepOptionChain, weights=weights)

                    OPS = synopsis.computeOptionPriceSpread()
                    IVS = synopsis.computeImpliedVolatilitySpread()
                    NAP = synopsis.computeNoArbitragePrice()
                    OIR = synopsis.computeOpenInterestRatio()

                    summary['OPS_[{}]'.format(mode)] = OPS.mean
                    summary['IVS_[{}]'.format(mode)] = IVS.mean
                    summary['NAP_[{}]'.format(mode)] = NAP.value
                    summary['NAP_ret_[{}]'.format(mode)] = NAP.ret
                    summary['OIR_[{}]'.format(mode)] = OIR.mean

                PCD = synopsis.computePutCallDelta()
                summary['PCD'] = PCD

                # Compute volatility metrics
                VIX = EquityVIX(deepOptionChain)
                summary['VIX_[hist]'] = VIX.getHistoricalVolatility()
                summary['VIX_[mean]'] = VIX.getMeanVIX().value
                summary['VIX_[beta]'] = VIX.getBetaVIX().value
                summary['VIX_[CBOE]'] = VIX.getCBOEVIX()

                if output.empty:
                    output = pd.DataFrame(columns=list(summary.keys()), index=[])

                output = output.append(summary, ignore_index=True)
        except Exception as e:
            logs.append('Error with [{}] - [{}]: {}'.format(ticker.ticker, now, e))
            pass

    # ----------------------[EXPORT BLOCK]--------------------------------
    path = '../Export/BackTest/{}'.format(ticker.ticker)
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        with pd.ExcelWriter('{}/backTest_[{}].xlsx'.format(path, maturity_min)) as writer:
            output.to_excel(writer, sheet_name='Results', index=False)
    except:
        pass
    # ----------------------[EXPORT BLOCK]--------------------------------


if __name__ == "__main__":
    if multiprocess:
        with Pool(processes=8) as p:
            with tqdm(total=len(ticker_list)) as pbar:
                for i, _ in enumerate(p.imap_unordered(execute, ticker_list)):
                    pbar.update()
    else:
        for tick in tqdm(ticker_list):
            execute(tick)

    with open('log.txt', 'w') as f:
        for item in logs:
            f.write("%s\n" % item)
