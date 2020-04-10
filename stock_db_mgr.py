# To make print working for Python2/3
from __future__ import print_function

# system
import datetime
import os

# custom
import pandas as pd

# user
import finance_utils as fu


# Defaults:
_default_start_date = datetime.date(1900, 1, 1)
_default_end_date = datetime.date.today()


class StockDBMgr(object):
    """Stock Data Base Manager: handles reading a list of stock CSV files from a storage directory."""

    def __init__(self, basedir, startDate=None, endDate=None, adjustPrice=True):
        """Instantiate the class."""
        if startDate is None:
            startDate = _default_start_date
        if endDate is None:
            endDate = _default_end_date
        self._basedir  = basedir
        self._startDate = startDate
        self._endDate = endDate
        self._dataDic = {}
        self._adjustPrice = adjustPrice

    def getAllSymbolsAvailable(self):
        """Return a list of ticker symbols corresponding to the data available locally on disk."""
        return fu.getAllSymbolsAvailable(self._basedir)

    def downloadData(self, symbol):
        """Download the data for the given symbol."""
        fu.downloadData(symbol, self._basedir, _default_start_date, _default_end_date)
        # Make sure the data is re-fetched from disk
        if symbol in self._dataDic:
            del self._dataDic[symbol]

    def validateSymbolData(self, symbol):
        """Perform basic data validation on symbol, return True/False based on the result."""
        return fu.validateSymbolData(fu.symbolToFilename(symbol, self._basedir))

    def updateAllSymbols(self):
        """Re-download all symbol data available on disk."""
        fu.updateAllSymbols(self._basedir, _default_start_date, _default_end_date)
        # Make sure the data is re-fetched from disk
        self._dataDic = {}

    def getSymbolData(self, symbol):
        """Return a single symbol data as a DataFrame."""
        if symbol not in self._dataDic:
            f = fu.symbolToFilename(symbol, self._basedir)
            if not os.path.exists(f):
                self.downloadData(symbol)
            df = fu.loadDataFrame(f, self._startDate, self._endDate, adjustPrice=self._adjustPrice)
            if df is None:
                print("ERROR: data for {} contains error".format(symbol))
            self._dataDic[symbol] = df  # Store it for next time
        # if data is already there, assume it is up to date (to save repetitive download)
        return self._dataDic[symbol]

    def getAllSymbolDataDic(self):
        # Update data dictionary cache
        for s in self.getAllSymbolsAvailable():
            self.getSymbolData(s)  # return is ignored on purpose
        return self._dataDic

    def getAllSymbolDataSingleItem(self, item):
        """Combine one item of all available stock into a single DataFrame.

        Available item are 'Open', 'High', 'Low', 'Close'.
        """

        # Re-index to only have the relevant date range
        date_range = pd.date_range(self._startDate, self._endDate, name='Date')

        dic = self.getAllSymbolDataDic()

        keys = dic.keys()
        keys.sort()

        df = pd.DataFrame(index=date_range)
        for k in keys:
            #print(len(dic[k][item]))
            df[k] = dic[k][item]

        # Discarding NaN values that are all NaN for a given row
        df.dropna(how='all', inplace=True)

        # Need to replace na if any
        if df.isna().any().any():
            #print(df.loc[df.isna().any(axis=1)])
            # Forward fill nan with last known good value.
            # This will ensure all days have values
            df.fillna(method='ffill', inplace=True, limit=5)
            if df.isna().any().any():
                print("Error: too many NAN: {}".format(df.columns[df.isna().sum() > 0]))

        # Axis naming
        df.rename_axis(item, axis='columns', inplace=True)

        return df


def _main():
    db = StockDBMgr('./stock_db/test', datetime.date(2017, 1, 1), datetime.date(2018, 1, 1))
    symbol_list = db.getAllSymbolsAvailable()
    print(symbol_list)

    # Work with first symbol only
    s = symbol_list[0]

    if False:
        # To test caching
        df = db.getSymbolData(s)
        df = db.getSymbolData(s)
        db.downloadData(s)
        df = db.getSymbolData(s)
        db.updateAllSymbols()
        df = db.getSymbolData(s)

    if True:
        print("Validating symbols")
        for s in db.getAllSymbolsAvailable():
            if not db.validateSymbolData(s):
                print("{} failed validation".format(s))

    if True:
        print("Loading all symbols to a dict")
        # To test caching
        dd = db.getAllSymbolDataDic()
        dd = db.getAllSymbolDataDic()
        print(dd.keys())

        df = db.getAllSymbolDataSingleItem('Close')
        print(df.head())
        df = db.getAllSymbolDataSingleItem('Volume')
        print(df.head())

    if True:
        db = StockDBMgr('./stock_db/test', datetime.date(2017, 1, 1), datetime.date(2018, 1, 1), adjustPrice=False)
        df = db.getSymbolData(symbol_list[0])
        print(df.describe())


if __name__ == '__main__':
    _main()
