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

# start_date = datetime.date(1900, 1, 1)

# Start of Questrade portfolio
start_date = datetime.date(2014, 1, 6)

# Start of Questrade portfolio component highest start date (VUN.TO)
# start_date = datetime.date(2013, 8, 12)

end_date = datetime.date.today()

# default
data_dir = './stock_db/qt'
# Global data dictionary
data_dic = {}
db = None


def calcCommissionETF(nbShare):
    """Return the ETF trade commission: positive=Buy, negative=Sell."""
    return (nbShare < 0) * min(9.95, max(4.95, -nbShare * 0.01)) + math.fabs(nbShare) * 0.0035


def simulate():
    print("simulate()")

    initialCash = 100000.0
    a = va.VirtualAccount(initialCash, data_dic)

    print("Initial cash", a.get_cash())

    # Target allocation:
    ratio = {
        'XBB.TO': 0.1,
        'ZCN.TO': 0.3,
        'VUN.TO': 0.3,
        'XEF.TO': 0.2,
        'XEC.TO': 0.1
    }

    # Symbol loop
    symbolList = data_dic.keys()
    symbolList.sort()

    df = pd.DataFrame(
        index=symbolList,
        data=[ratio[s] for s in symbolList],
        columns=['TgtAlloc'])

    df['NbShare'] = np.zeros(len(symbolList))

    dfPrices = db.getAllSymbolDataSingleItem('Close')
    for i in range(len(dfPrices)):
        if i % 100 == 0: # Adjust rebalance frequency
            print("Rebalance", i)

            # Roughly Matching StockPortfolio_RRSP column ordering

            df['Price'] = dfPrices.iloc[i]

            df['MktValue'] = df['Price'] * df['NbShare']

            totalValue = sum(df['Price'] * df['NbShare']) + a.get_cash()

            df['CurrAlloc'] = df['MktValue'] / totalValue
            df['DeltaAlloc'] = df['CurrAlloc'] - df['TgtAlloc']

            df['TgtValue'] = df['TgtAlloc'] * totalValue

            # +:Buy  -:Sell
            df['DeltaShare'] = np.floor((df['TgtValue']) / df['Price']) - df['NbShare']

            c = [calcCommissionETF(n) for n in df['DeltaShare'].values]

            # TBD not sure about the commission formula for both buy & sell...

            for s in symbolList:
                n = df.loc[s, 'DeltaShare']
                if n > 0:
                    print("  Buy {} of {}".format(n, s))
                    a.delta_cash(-n * df.loc[s, 'Price'])
                    df.loc[s, 'NbShare'] += n
                    #a.buy_at_market(i, s, n)
                elif n < 0:
                    print("  Sell {} of {}".format(-n, s))
                    a.delta_cash(-n * df.loc[s, 'Price'])
                    df.loc[s, 'NbShare'] += n
                    #a.sell_at_market()

            # Do not tolerate after all transactions are done.
            if a.get_cash() < 0:
                print("Error: not enough money", a.get_cash())

        else:
            #print("skip", i)
            pass

    print("Initial Cash =", initialCash)
    # Update last price
    df['Price'] = [data_dic[s].iloc[-1]['Close'] for s in symbolList]
    print("Final Cash = ", sum(df['Price'] * df['NbShare']) + a.get_cash())


def simulate2():
    print("simulate()")

    a = va.VirtualAccount(50000.00, data_dic)

    print("Initial cash", a.get_cash())

    # Symbol loop
    symbolList = data_dic.keys()
    symbolList.sort()
    for crtSymbol in symbolList:
        print("Simulating with", crtSymbol)
        crtBars = data_dic[crtSymbol]

        # The various series (starting with s):
        # sOpen = fu.getOpen(crtBars)
        # sHigh = fu.getHigh(crtBars)
        # sLow = fu.getLow(crtBars)
        sClose = fu.getClose(crtBars)
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
            openPositions = a.get_open_positions(crtSymbol)
            for pos in openPositions:
                # TBD sell logic
                sellSignal = sClose[bar] > 1.15 * pos.get_entry_price() or \
                             sClose[bar] < 0.95 * pos.get_entry_price()
                if sellSignal:
                    a.sell_at_market(pos, bar + 1) # bar + 1 = tomorrow
            if not openPositions:
                # TBD buy logic
                buySignal = ti.cross_over(sClose, sCloseSma)[bar]
                if buySignal:
                    nbShare = int(2500 / sClose[bar]) # 2500$ => about 0.8% commission buy + sell
                    a.buy_at_market(bar + 1, crtSymbol, nbShare) # bar + 1 = tomorrow

    for p in a.get_all_positions():
        print(p)

    print("Final cash", a.get_cash())


def plotTest():
    print("plotTest()")

    symbolList = data_dic.keys()
    symbolList.sort()
    for crtSymbol in symbolList:
        print("Plotting with " + crtSymbol)
        df = data_dic[crtSymbol]

        X = fu.getClose(df)
        t = np.arange(len(X))
        plt.plot(t, X,)
        #plt.plot(t, ti.sma(X, 200))
        #plt.plot(t, ti.ema(X, 200))
        #plt.plot(t, ti.linFit(X, 200))
        plt.plot(t, ti.iir_lowpass(X, 3, 200))
        #plt.plot(t, ti.aema(X, 200))
        plt.grid(True)
        plt.show()


def loadData():
    print("loadData()")

    global data_dic
    global db

    db = sdm.StockDBMgr(data_dir, start_date, end_date)

    data_dic = db.getAllSymbolDataDic()


def _main():
    print("main()")

    global data_dir

    # parse arguments
    parser = OptionParser()
    parser.add_option("-d", "--dir", dest="dataDir", action="store", default=data_dir,
        help="Get stock data (CSV) from this directory, it uses " + data_dir + " as default")
    (options, _args) = parser.parse_args()
    data_dir = options.dataDir

    loadData()

    plotTest()

    simulate()
    # simulate2()


if __name__ == '__main__':
    _main()

