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
    """Stock Data Base Manager: handles stock data stored in CSV files."""

    def __init__(self, basedir, start_date=None, end_date=None, adjust_price=True):
        """Instantiate the class."""
        if start_date is None:
            start_date = _default_start_date
        if end_date is None:
            end_date = _default_end_date
        self._basedir = basedir
        self._start_date = start_date
        self._end_date = end_date
        self._dic = {}
        self._adjust_price = adjust_price

    def get_all_symbols(self):
        """Return a list of ticker symbols corresponding to the data available locally on disk."""
        return fu.get_all_symbols(self._basedir)

    def download_data(self, symbol):
        """Download the data for the given symbol and store it in the DB basedir."""
        fu.download_data(symbol, self._basedir, _default_start_date, _default_end_date)
        # Make sure the data is re-fetched from disk (clear cache).
        if symbol in self._dic:
            del self._dic[symbol]

    def validate_symbol_data(self, symbol):
        """Perform basic data validation on symbol, return True/False based on the result."""
        return fu.validate_symbol_data(fu.symbol_to_filename(symbol, self._basedir))

    def update_all_symbols(self):
        """Re-download all symbol data available on disk."""
        fu.update_all_symbols(self._basedir, _default_start_date, _default_end_date)
        # Make sure the data is re-fetched from disk
        self._dic = {}

    def get_symbol_data(self, symbol):
        """Return a single symbol data as a DataFrame."""
        if symbol not in self._dic:
            f = fu.symbol_to_filename(symbol, self._basedir)
            if not os.path.exists(f):
                self.download_data(symbol)
            df = fu.load_data_frame(f, self._start_date, self._end_date, adjust_price=self._adjust_price)
            if df is None:
                print("ERROR: data for {} contains error".format(symbol))
            self._dic[symbol] = df  # Store it for next time
        # if data is already there, assume it is up to date (to save repetitive download)
        return self._dic[symbol]

    def get_all_symbol_data(self):
        """Return a dictionary of all symbols DataFrame."""
        # Update the dictionary cache
        for s in self.get_all_symbols():
            self.get_symbol_data(s)  # return is ignored on purpose
        return self._dic

    def get_all_symbol_single_data_item(self, data_item, fill_data=False):
        """Combine one data data_item of all available stock into a single DataFrame.

        Available data items are:
        - 'Open'
        - 'High'
        - 'Low'
        - 'Close'
        - 'Adj Close' (only when the DB is not adjusted)
        """
        # Re-index to only have the relevant date range
        date_range = pd.date_range(self._start_date, self._end_date, name='Date')

        dic = self.get_all_symbol_data()

        keys = dic.keys()
        keys.sort()

        df = pd.DataFrame(index=date_range)
        for k in keys:
            df[k] = dic[k][data_item]

        # Discarding NaN values that are all NaN for a given row
        df.dropna(how='all', inplace=True)

        if fill_data and df.isna().any().any():
            # print(df.loc[df.isna().any(axis=1)])

            # Data filling is done in 2 steps
            # 1. Fill forward nan with last known good value.
            df.fillna(method='ffill', inplace=True)
            # 2. Fill baward nan with first known good value.
            df.fillna(method='backfill', inplace=True)
            if df.isna().any().any():
                print("Error: too many NAN: {}".format(df.columns[df.isna().sum() > 0]))

        # Axis naming
        df.rename_axis(data_item, axis='columns', inplace=True)

        return df


def _main():
    db = StockDBMgr('./stock_db/test', datetime.date(2017, 1, 1), datetime.date(2018, 1, 1))
    symbol_list = db.get_all_symbols()
    print(symbol_list)

    # Work with first symbol only
    s = symbol_list[0]

    if False:
        # To test caching
        df = db.get_symbol_data(s)
        df = db.get_symbol_data(s)
        db.download_data(s)
        df = db.get_symbol_data(s)
        db.update_all_symbols()
        df = db.get_symbol_data(s)

    if True:
        print("Validating symbols")
        for s in db.get_all_symbols():
            if not db.validate_symbol_data(s):
                print("{} failed validation".format(s))

    if True:
        print("Loading all symbols to a dict")
        # To test caching
        dd = db.get_all_symbol_data()
        dd = db.get_all_symbol_data()
        print(dd.keys())

        df = db.get_all_symbol_single_data_item('Close')
        print(df.head())
        df = db.get_all_symbol_single_data_item('Volume')
        print(df.head())

    if True:
        db = StockDBMgr('./stock_db/test',
                        datetime.date(2017, 1, 1), datetime.date(2018, 1, 1), False)
        df = db.get_symbol_data(symbol_list[0])
        print(df.describe())


if __name__ == '__main__':
    _main()
