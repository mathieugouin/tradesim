# NOTES:
# http://stats.stackexchange.com/questions/1595/python-as-a-statistics-workbench
# http://en.wikipedia.org/wiki/Algorithmic_trading

# To make print working for Python2/3
from __future__ import print_function

import math
import datetime
from optparse import OptionParser

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import finance_utils as fu
import technical_indicators as ti
import stock_db_mgr as sdm
import virtual_account as va

startDate = datetime.date(1900, 1, 1)
startDate = datetime.date(2014, 1, 6) # Start of Questrade portfolio
startdate = datetime.date(2013, 8, 12) # Start of Questrade portfolio component highest start date (VUN.TO)
endDate = datetime.date.today()

# default
dataDir = './stock_db/qt'
# Global data dictionary
dataDic = {}
db = None


# +:Buy
# -:Sell
def calcCommissionETF(nbShare):
    #       (V2 < 0)     * min(9.95, max(4.95, -V2 * 0.01))     + abs(V2) * 0.0035
    return (nbShare < 0) * min(9.95, max(4.95, -nbShare * 0.01)) + math.fabs(nbShare) * 0.0035


def simulate():
    print("simulate()")

    initialCash = 100000.0
    a = va.VirtualAccount(initialCash, dataDic)

    print("Initial cash", a.getCash())

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

    df = pd.DataFrame(
        index = symbolList,
        data = [ratio[s] for s in symbolList],
        columns = ['TgtAlloc'])

    df['NbShare'] = np.zeros(len(symbolList))

    dfPrices = db.getAllSymbolDataSingleItem('Close')
    for i in range(len(dfPrices)):
        if i % 100 == 0: # Adjust rebalance frequency
            print("Rebalance", i)

            # Roughly Matching StockPortfolio_RRSP column ordering

            df['Price'] = dfPrices.iloc[i]

            df['MktValue'] = df['Price'] * df['NbShare']

            totalValue = sum(df['Price'] * df['NbShare']) + a.getCash()

            df['CurrAlloc'] = df['MktValue'] / totalValue
            df['DeltaAlloc'] = df['CurrAlloc'] - df['TgtAlloc']

            df['TgtValue'] = df['TgtAlloc'] * totalValue

            # +:Buy  -:Sell
            df['DeltaShare'] = np.floor((df['TgtValue']) / df['Price']) - df['NbShare']

            #c = [calcCommissionETF(n) for n in df['DeltaShare'].values]

            # TBD not sure about the commission formula for both buy & sell...

            for s in symbolList:
                n = df.loc[s, 'DeltaShare']
                if n > 0:
                    print("  Buy {} of {}".format(n, s))
                    a.deltaCash(-n * df.loc[s, 'Price'])
                    df.loc[s, 'NbShare'] += n
                    #a.buyAtMarket(i, s, n)
                elif n < 0:
                    print("  Sell {} of {}".format(-n, s))
                    a.deltaCash(-n * df.loc[s, 'Price'])
                    df.loc[s, 'NbShare'] += n
                    #a.sellAtMarket()

            # Do not tolerate after all transactions are done.
            if a.getCash() < 0:
                print("Error: not enough money", a.getCash())

        else:
            #print("skip", i)
            pass

    print("Initial Cash =", initialCash)
    # Update last price
    df['Price'] = [dataDic[s].iloc[-1]['Close'] for s in symbolList]
    print("Final Cash = ", sum(df['Price'] * df['NbShare']) + a.getCash())


def simulate2():
    print("simulate()")

    a = va.VirtualAccount(50000.00, dataDic)

    print("Initial cash", a.getCash())

    # Symbol loop
    symbolList = dataDic.keys()
    symbolList.sort()
    for crtSymbol in symbolList:
        print("Simulating with", crtSymbol)
        crtBars = dataDic[crtSymbol]

        # The various series (starting with s):
        # sOpen   = fu.getOpen(crtBars)
        # sHigh   = fu.getHigh(crtBars)
        # sLow    = fu.getLow(crtBars)
        sClose  = fu.getClose(crtBars)
        # sVolume = fu.getVolume(crtBars)

        # Technical indicators
        # sVolumeSma = ti.sma(sVolume, 21)
        sCloseSma = ti.sma(sClose, 200)
        # sCloseEma = ti.ema(sClose, 200)

        # Bar loops (1 bar per day)
        # start index to include various moving average lag
        # end at -1 to include "tomorrow" (corresponds to last valid bar)
        # TBD to fix this with real signals
        for bar in range(200, len(crtBars) - 1):
            # barObj = crtBars.iloc[bar]

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
                    nbShare = int(2500 / sClose[bar]) # 2500$ => about 0.8% commission buy + sell
                    a.buyAtMarket(bar + 1, crtSymbol, nbShare) # bar + 1 = tomorrow

    for p in a.getAllPositions():
        print(p)

    print("Final cash", a.getCash())


def plotTest():
    print("plotTest()")

    symbolList = dataDic.keys()
    symbolList.sort()
    for crtSymbol in symbolList:
        print("Plotting with " + crtSymbol)
        df = dataDic[crtSymbol]

        X = fu.getClose(df)
        t = np.arange(len(X))
        plt.plot(t, X,)
        #plt.plot(t, ti.sma(X, 200))
        #plt.plot(t, ti.ema(X, 200))
        #plt.plot(t, ti.linFit(X, 200))
        plt.plot(t, ti.iir(X, 3, 200))
        #plt.plot(t, ti.aema(X, 200))
        plt.grid(True)
        plt.show()


def loadData():
    print("loadData()")

    global dataDic
    global db

    db = sdm.StockDBMgr(dataDir, startDate, endDate)

    dataDic = db.getAllSymbolDataDic()


def _main():
    print("main()")

    global dataDir

    # parse arguments
    parser = OptionParser()
    parser.add_option("-d", "--dir", dest="dataDir", action="store", default=dataDir,
                      help="Get stock data (csv) from this directory, it uses " + dataDir + " as default")
    (options, _args) = parser.parse_args()
    dataDir = options.dataDir

    loadData()

    #plotTest()

    simulate()
    #simulate2()


if __name__ == '__main__':
    _main()
