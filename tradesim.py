# NOTES:
# http://stats.stackexchange.com/questions/1595/python-as-a-statistics-workbench
# http://en.wikipedia.org/wiki/Algorithmic_trading

import datetime
import re
import glob
import os
from optparse import OptionParser

import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt

from Bar import *
from Position import *
import technical_indicators as ti
import gstockquote as gsq
import ystockquote as ysq

startDate = datetime.date(1900, 1, 1)
#endDate = datetime.date(2012, 12, 1)
endDate = datetime.date.today() #.today() #now()

options = 0

# default
dataDir = r'.\stock_db\test'
# Global data dictionary
dataDic = {}



###############################################################################
class CVirtualAccount:
    def __init__(self, initialCapital, commission = 9.95):
        self._initialCapital    = initialCapital
        self._cash              = self._initialCapital
        self._commission        = commission
        self._positions         = []

    def buyAtMarket(self, bar, symbol, nbShare, name = "buyAtMarket"):
        print "buyAtMarket()"
        #buyPrice = dataDic[symbol][bar].open
        buyPrice = dataDic[symbol][bar].high # Worst case simulation
        nbShare = int(nbShare)
        cost = buyPrice * nbShare + self._commission;
        if cost < self._cash:
            self._positions.append(CPosition(bar, symbol, nbShare, buyPrice, name, self._commission))
            self._cash -= cost
        else:
            print "Error: not enough money"

    def sellAtMarket(self, position, bar, name = "sellAtMarket"):
        print "sellAtMarket()"
        #sellPrice = dataDic[position.getSymbol()][bar].close
        sellPrice = dataDic[position.getSymbol()][bar].low # Worst case
        cost = self._commission;
        if cost < self._cash:
            self._cash -= cost
            self._cash += position.close(bar, sellPrice, name)
        else:
            print "Error: not enough money"

    def getAllPositions(self, symbol = ""):
        if symbol in dataDic.keys():
            return [p for p in self._positions if p.getSymbol() == symbol] # positions only for symbol
        else:
            return [p for p in self._positions] # all positions

    def getOpenPositions(self, symbol = ""):
        if symbol in dataDic.keys():
            return [p for p in self._positions if p.getSymbol() == symbol and p.isOpen()] # open positions only for symbol
        else:
            return [p for p in self._positions if p.isOpen()] # all open positions

    def getClosePositions(self, symbol = ""):
        if symbol in dataDic.keys():
            return [p for p in self._positions if p.getSymbol() == symbol and not p.isOpen()] # close positions only for symbol
        else:
            return [p for p in self._positions if not p.isOpen()] # all close positions

    def getCash(self):
        return self._cash

###############################################################################
def simulate():
    print "simulate()"

    va = CVirtualAccount(50000, 9.95)

    print "Initial cash", va.getCash()

    # Symbol loop
    symbolList = dataDic.keys()
    symbolList.sort()
    for crtSymbol in symbolList:
        print "Simulating with", crtSymbol
        crtBars = dataDic[crtSymbol]

        # The various series (starting with s):
        sOpen   = np.array([b.open   for b in crtBars], dtype=np.float64)
        sHigh   = np.array([b.high   for b in crtBars], dtype=np.float64)
        sLow    = np.array([b.low    for b in crtBars], dtype=np.float64)
        sClose  = np.array([b.close  for b in crtBars], dtype=np.float64)
        sVolume = np.array([b.volume for b in crtBars], dtype=np.float64)

        # Technical indicators
        sVolumeSma = ti.sma(sVolume, 21)
        sCloseSma = ti.sma(sClose, 200)
        sCloseEma = ti.ema(sClose, 200)

        # Bar loops (1 bar per day)
        # start index to include various moving average lag
        # end at -1 to include "tomorrow" (corresponds to last valid bar)
        # TBD to fix this with real signals
        for bar in range(200, len(crtBars) - 1):
            barObj = crtBars[bar]
            #date = barObj.date

            # Positions loop
            openPositions = va.getOpenPositions(crtSymbol)
            for pos in openPositions:
                # TBD sell logic
                sellSignal = sClose[bar] > 1.15 * pos.getEntryPrice() or \
                             sClose[bar] < 0.95 * pos.getEntryPrice()
                if sellSignal:
                    va.sellAtMarket(pos, bar + 1) # bar + 1 = tomorrow
            if not openPositions:
                # TBD buy logic
                buySignal = ti.crossOver(sClose, sCloseSma, bar)
                if buySignal:
                    nbShare = int(2500 / sClose[bar]) # 2500$ => about 0.8% comission buy + sell
                    va.buyAtMarket(bar + 1, crtSymbol, nbShare) # bar + 1 = tomorrow

    print "Final cash", va.getCash()
    #print "Entering debugger..."; import pdb; pdb.set_trace()


###############################################################################
def plotTest():
    print "plotTest()"

    symbolList = dataDic.keys()
    symbolList.sort()
    for crtSymbol in symbolList:
        print "Plotting with", crtSymbol
        crtBars = dataDic[crtSymbol]

        X = np.array([b.close  for b in crtBars], dtype=np.float64)
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

    global dataDir
    global dataDic

    if dataDir[-1] == '\\':
        dataDir = dataDir[0:-2]

#    for csvFile in glob.glob(os.path.join(dataDir, '*.csv')):
#        bars = [] # array
#        print "Loading data from: " + csvFile
#        symbol = os.path.basename(csvFile).replace('.csv', '')
#        #print "> %s" % gsq.get_company_name(symbol)
#
#        # The CSV files are downloaded from yahoo historical data
#        f = open(csvFile, 'r')
#        #lineSplit  0,   1,   2,   3,  4,    5,     6
#        #priceData       0,   1,   2,  3,    4,     5
#        #           Date,Open,High,Low,Close,Volume,Adj Close
#        #           2012-03-21,204.32,205.77,204.30,204.69,3329900,204.69
#        f.seek(0)
#        f.readline() # skip header row
#        for l in f.readlines():
#            # Date,Open,High,Low,Close,Volume,Adj Close
#            lineSplit = l.strip().split(',')
#            if len(lineSplit) != 7:
#                print "Error: Invalid line"
#                continue
#            dateSplit = map(int, lineSplit[0].split('-'))
#            date = datetime.date(dateSplit[0], dateSplit[1], dateSplit[2])
#            # Yahoo CSV data is most recent first
#            if date < startDate: # Data starting with this line in the file is too old
#                break # stop processing this file
#            if startDate <= date and date <= endDate:
#                priceData = map(float, lineSplit[1:])
#                adjRatio = priceData[5] / priceData[3] # Adj Close / Close
#
#                # %Adjust for dividends, splits, etc.
#                # DATEtemp{ptr,1} = DATEvar;
#                # OPENtemp(ptr,1) = OPENvar  * adj_close / CLOSEvar;
#                # HIGHtemp(ptr,1) = HIGHvar  * adj_close / CLOSEvar;
#                # LOWtemp (ptr,1) = LOWvar   * adj_close / CLOSEvar;
#                # CLOSEtemp(ptr,1)= CLOSEvar * adj_close / CLOSEvar;
#                # VOLtemp(ptr,1)  = VOLvar;
#
#                bar = CBar(
#                            date,
#                            priceData[0] * adjRatio, # open
#                            priceData[1] * adjRatio, # high
#                            priceData[2] * adjRatio, # low
#                            priceData[3] * adjRatio, # close
#                            priceData[4]             # volume (in nb of shares)
#                         )
#                bars.append(bar)
#        f.close()
#        bars.reverse() # now bars[0] is the earliest

        dataDic[symbol] = bars


###############################################################################
def main():
    print "main()"

    global dataDir
    global options

    # parse arguments
    parser = OptionParser()
    parser.add_option("-d", "--dir", dest="dataDir", action="store", default = dataDir,
                      help="Get stock data (csv) from this directory, it uses " + dataDir + " as default")
    (options, args) = parser.parse_args()
    dataDir = options.dataDir

    loadData()

    plotTest()

    #simulate()

if __name__ == '__main__':
    main()
