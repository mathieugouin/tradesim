# NOTES:
# http://stats.stackexchange.com/questions/1595/python-as-a-statistics-workbench
# http://en.wikipedia.org/wiki/Algorithmic_trading

import math
import datetime
import re
import glob
import os
from optparse import OptionParser

import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

from Bar import *
from Position import *
import technical_indicators as ti
import gstockquote as gsq
import ystockquote as ysq
import tmxstockquote as tmx
import stock_db_mgr as sdm
import VirtualAccount as va

startDate = datetime.date(1900, 1, 1)
startDate = datetime.date(2014, 1, 6) # Start of Questrade portfolio
#endDate = datetime.date(2012, 12, 1)
endDate = datetime.date.today() #.today() #now()

options = 0

# default
dataDir = './stock_db/qt'
# Global data dictionary
dataDic = {}

# +:Buy
# -:Sell
def calcCommissionETF(nbShare):
    #       (V2 < 0)     * min(9.95, max(4.95, -V2 * 0.01))     + abs(V2) * 0.0035
    return (nbShare < 0) * min(9.95, max(4.95, -nbShare * 0.01)) + math.fabs(nbShare) * 0.0035

###############################################################################
def simulate():
    print "simulate()"

    a = va.CVirtualAccount(100000.00, dataDic)

    print "Initial cash", a.getCash()

    # Target allocation:
    ratio = {
        'XBB.TO': 0.1,
        'ZCN.TO': 0.3,
        'VUN.TO': 0.3,
        'XEF.TO': 0.2,
        'XEC.TO': 0.1
    }

    # Symbol loop
    symbolList = dataDic.keys()
    symbolList.sort()
    for i in range(max([len(dataDic[s]) for s in symbolList])):
        if i % 20 == 0: # TBD rebalance freq
            print "rebalance", i
            vDic = {}
            nbShDic = {}

            # Matching StockPortfolio_RRSP column ordering

            df = pd.DataFrame(
                index = symbolList,
                data = [dataDic[s].ix[i, 'High'] for s in symbolList],
                columns=['Price'])

            df['NbShare'] = [sum([p.getNbShare() for p in a.getOpenPositions(s)]) for s in symbolList]
            df['MktValue'] = df['Price'] * df['NbShare']
            df['TgtAlloc'] = [ratio[s] for s in symbolList]  # could be moved above and be done only once

            totalValue = sum(df['Price'] * df['NbShare']) + a.getCash()

            df['CurrAlloc'] = df['MktValue'] / totalValue
            df['DeltaAlloc'] = df['CurrAlloc'] - df['TgtAlloc']

            df['TgtValue'] = df['TgtAlloc'] * totalValue

            # +:Buy  -:Sell
            df['DeltaShare'] = np.floor((df['TgtValue']) / df['Price']) - df['NbShare']

            c = [calcCommissionETF(n) for n in df['DeltaShare'].values]

            # TBD not sure about the commission formula for both buy & sell...

            # TBD rework buy / sell to work with partial position buy & sell
            if False:
                for s in symbolList:
                    n = df.ix[s, 'DeltaShare']
                    if n > 0:
                        a.buyAtMarket(i, s, n)
                    else:
                        #va.sellAtMarket()
                        pass
        else:
            print "skip", i
            pass

    print "Final cash", a.getCash()
    #print "Entering debugger..."; import pdb; pdb.set_trace()


###############################################################################
def simulate2():
    print "simulate()"

    a = va.CVirtualAccount(50000.00, dataDic)

    print "Initial cash", a.getCash()

    # Symbol loop
    symbolList = dataDic.keys()
    symbolList.sort()
    for crtSymbol in symbolList:
        print "Simulating with", crtSymbol
        crtBars = dataDic[crtSymbol]

        # The various series (starting with s):
        sOpen   = sdm.getOpen(crtBars)
        sHigh   = sdm.getHigh(crtBars)
        sLow    = sdm.getLow(crtBars)
        sClose  = sdm.getClose(crtBars)
        sVolume = sdm.getVolume(crtBars)

        # Technical indicators
        sVolumeSma = ti.sma(sVolume, 21)
        sCloseSma = ti.sma(sClose, 200)
        sCloseEma = ti.ema(sClose, 200)

        # Bar loops (1 bar per day)
        # start index to include various moving average lag
        # end at -1 to include "tomorrow" (corresponds to last valid bar)
        # TBD to fix this with real signals
        for bar in range(200, len(crtBars) - 1):
            barObj = crtBars.iloc[bar]
            #date = barObj.date

            # Positions loop
            openPositions = a.getOpenPositions(crtSymbol)
            for pos in openPositions:
                # TBD sell logic
                sellSignal = sClose[bar] > 1.15 * pos.getEntryPrice() or \
                             sClose[bar] < 0.95 * pos.getEntryPrice()
                if sellSignal:
                    a.sellAtMarket(pos, bar + 1) # bar + 1 = tomorrow
            if not openPositions:
                # TBD buy logic
                buySignal = ti.crossOver(sClose, sCloseSma, bar)
                if buySignal:
                    nbShare = int(2500 / sClose[bar]) # 2500$ => about 0.8% comission buy + sell
                    a.buyAtMarket(bar + 1, crtSymbol, nbShare) # bar + 1 = tomorrow

    for p in a.getAllPositions():
        print p.toString()

    print "Final cash", a.getCash()
    #print "Entering debugger..."; import pdb; pdb.set_trace()


###############################################################################
def plotTest():
    print "plotTest()"

    symbolList = dataDic.keys()
    symbolList.sort()
    for crtSymbol in symbolList:
        print "Plotting with", crtSymbol
        df = dataDic[crtSymbol]

        X = sdm.getClose(df)
        t = np.arange(len(X))
        plt.plot(t, X,)
        #plt.plot(t, ti.sma(X, 200))
        #plt.plot(t, ti.ema(X, 200))
        #plt.plot(t, ti.linFit(X, 200))
        plt.plot(t, ti.iir(X, 3, 200))
        #plt.plot(t, ti.aema(X, 200))
        plt.grid(True)
        plt.show()


###############################################################################
def loadData():
    print "loadData()"

    global dataDic

    db = sdm.CStockDBMgr(dataDir, startDate, endDate)

    dataDic = db.getAllSymbolDataDic()


###############################################################################
def _main():
    print "main()"

    global dataDir
    global options

    # parse arguments
    parser = OptionParser()
    parser.add_option("-d", "--dir", dest="dataDir", action="store", default=dataDir,
                      help="Get stock data (csv) from this directory, it uses " + dataDir + " as default")
    (options, args) = parser.parse_args()
    dataDir = options.dataDir

    loadData()

    #plotTest()

    simulate()
    #simulate2()

if __name__ == '__main__':
    _main()
