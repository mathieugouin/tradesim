#-------------------------------------------------------------------------------
# Name:        Stock Data Base Manager
# Purpose:
#
# Author:      Mathieu Gouin
#-------------------------------------------------------------------------------

# system
import datetime
import time
import os

# custom
import numpy as np
#from matplotlib.finance import parse_yahoo_historical
import pandas as pd

# user
import Bar
import finance_utils as fu


# Defaults:
_defStartDate = datetime.date(1900, 1, 1)
_defEndDate = datetime.date.today()

#-------------------------------------------------------------------------------
# Utils
def getDate(df):
    #return df.index.values
    return [i.date() for i in df.index]

def getOpen(df):
    return df['Open'].values

def getHigh(df):
    return df['High'].values

def getLow(df):
    return df['Low'].values

def getClose(df):
    return df['Close'].values

def getVolume(df):
    return df['Volume'].values

#-------------------------------------------------------------------------------
class CStockDBMgr:
    def __init__(self, basedir, startDate=None, endDate=None):
        if startDate is None:
            startDate = _defStartDate
        if endDate is None:
            endDate = _defEndDate
        self._basedir   = basedir
        self._startDate = startDate
        self._endDate   = endDate
        self._wp        = None
        self._dataDic   = None

    def getAllSymbolsAvailable(self):
        return fu.getAllSymbolsAvailable(self._basedir)

    def downloadData(self, symbol):
        fu.downloadData(symbol, self._basedir, self._startDate, self._endDate)

    def updateAllSymbols(self):
        fu.updateAllSymbols(self._basedir, self._startDate, self._endDate)

    def getSymbolData(self, symbol):
        f = fu.symbolToFilename(symbol, self._basedir)
        if (not os.path.exists(f)):
            fu.downloadData(symbol, self._basedir, self._startDate, self._endDate)
        # if data is already there, assume it is up to date (to save repetitive download)

        df = fu.loadDataFrame(f, self._startDate, self._endDate)
        return df


    def getAllSymbolDataDic(self):
        # Load it once
        if self._dataDic is None:
            t0 = time.clock()
            self._dataDic = {}
            for s in self.getAllSymbolsAvailable():
                print "Loading " + s + " ..."
                df = self.getSymbolData(s)
                #print df.shape[0]
                self._dataDic[s] = df
            dt = time.clock() - t0
            print "Load time:", dt

            noneKeys = [k for k in self._dataDic.keys() if self._dataDic[k] is None]
            for k in noneKeys:
                print "Removing {} as it contains error".format(k)
                del self._dataDic[k]

        return self._dataDic

    # Deprecated
    def getAllSymbolData(self):
        # Load it once
        if self._wp is None:
            t0 = time.clock()
            dic = self.getAllSymbolDataDic()
            dt = time.clock() - t0
            self._wp = pd.Panel(dic)
            print "Load time:", dt

        return self._wp

    def getAllSymbolDataSingleItem(self, item):
        # Re-index to only have the relevant date range
        dateRange = pd.date_range(self._startDate, self._endDate)

        dic = self.getAllSymbolDataDic()

        keys = dic.keys()
        keys.sort()

        df = pd.DataFrame(index=dateRange)
        for k in keys:
            #print len(dic[k][item])
            df[k] = dic[k][item]

        # Discarding NaN values that are all NaN for a given row
        df.dropna(how='all', inplace=True)

        # Need to replace na if any
        if df.isna().any().any():
            #print df.loc[df.isna().any(axis=1)]
            # Forward fill nan with last known good value.
            # This will ensure all days have values
            df.fillna(method='ffill', inplace=True, limit=5)
            if df.isna().any().any():
                print "Error: too many NAN: {}".format(df.columns[df.isna().sum() > 0])

        return df


    def validateSymbolData(self, symbol):
        return fu.validateSymbolData(fu.symbolToFilename(symbol, self._basedir))

#-------------------------------------------------------------------------------
def _main():
    db = CStockDBMgr('./stock_db/qt', datetime.date(2017, 1, 1), datetime.date(2018, 1, 1))
    #db = CStockDBMgr('./stock_db/test')
    #db.updateAllSymbols()
    symbolList = db.getAllSymbolsAvailable()
    print symbolList

    # Do with only first symbol
    s = symbolList[0]
    print s, 'Valid? : ', db.validateSymbolData(s)
    df = db.getSymbolData(s)

    if False:
        print getDate(df)[0]
        print getOpen(df)[0]
        print getHigh(df)[0]
        print getLow(df)[0]
        print getClose(df)[0]
        print getVolume(df)[0]

    if False:
        print "Validating symbols"
        t0 = time.clock()
        for s in db.getAllSymbolsAvailable():
            if not db.validateSymbolData(s):
                print s, " failed validation"
        dt = time.clock() - t0
        print dt

    if True:
        print "Loading all symbols to a dict"
        dd = db.getAllSymbolDataDic()
        #print dd

        df = db.getAllSymbolDataSingleItem('Close')
        pass
        #print df

    if True:
        print "Loading all symbols to a panel"
        wp = db.getAllSymbolData()
        print wp


if __name__ == '__main__':
    _main()
