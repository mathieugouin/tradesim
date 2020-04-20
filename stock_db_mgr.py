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

    def get_all_symbol_single_data_item(self, data_item):
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

        # Axis naming
        df.rename_axis(data_item, axis='columns', inplace=True)

        return df
