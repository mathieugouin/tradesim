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
import pandas as pd

# user
import finance_utils as fu


# Defaults:
_defStartDate = datetime.date(1900, 1, 1)
_defEndDate = datetime.date.today()


# Utils
# TBD move this to finance utils??
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
        """Return a list of ticker symbols corresponding to the data available locally on disk."""
        return fu.getAllSymbolsAvailable(self._basedir)

    def downloadData(self, symbol):
        """Download the data for the given symbol."""
        fu.downloadData(symbol, self._basedir, self._startDate, self._endDate)

    def updateAllSymbols(self):
        """Re-download all symbol data available on disk."""
        fu.updateAllSymbols(self._basedir, self._startDate, self._endDate)

    def getSymbolData(self, symbol):
        """Return a single symbol data as a DataFrame."""
        f = fu.symbolToFilename(symbol, self._basedir)
        if not os.path.exists(f):
            self.downloadData(symbol)
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
                # print df.shape[0]
                if df is not None:
                    self._dataDic[s] = df
                else:
                    print "ERROR: data for {} contains error, skipping".format(s)
            dt = time.clock() - t0
            print "Load time:", dt

        return self._dataDic

    # TBD Deprecated because it uses Pandas panel
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
        """Combine one item of all available stock into a single DataFrame.
        Available item are 'Open', 'High', 'Low', 'Close'."""
        # Re-index to only have the relevant date range
        date_range = pd.date_range(self._startDate, self._endDate)

        dic = self.getAllSymbolDataDic()

        keys = dic.keys()
        keys.sort()

        df = pd.DataFrame(index=date_range)
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
    #db = CStockDBMgr('./stock_db/qt', datetime.date(2017, 1, 1), datetime.date(2018, 1, 1))
    db = CStockDBMgr('./stock_db/test')
    #db.updateAllSymbols()
    symbolList = db.getAllSymbolsAvailable()
    print symbolList

    # Do with only first symbol
    s = symbolList[0]
    print s, 'Valid? : ', db.validateSymbolData(s)
    df = db.getSymbolData(s)

    if True:
        print getDate(df)[0:3]
        print getOpen(df)[0:3]
        print getHigh(df)[0:3]
        print getLow(df)[0:3]
        print getClose(df)[0:3]
        print getVolume(df)[0:3]

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
        print df.head()
        pass

    if True:
        print "Loading all symbols to a panel"
        wp = db.getAllSymbolData()
        print wp


if __name__ == '__main__':
    _main()
