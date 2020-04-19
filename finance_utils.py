"""Finance utilities library."""

# To make print working for Python2/3
from __future__ import print_function

# System
import re
import os
import glob
import urllib
import datetime
import csv
import time

# Custom
import pandas as pd

# User
import yqd


def filename_to_symbol(filename):
    """Return the basename of the filename without the .csv at the end."""
    pat = re.compile(re.escape('.csv'), re.IGNORECASE)
    return pat.sub('', os.path.basename(filename))


def symbol_to_filename(symbol, basedir):
    """Return the complete filename path based on the symbol and basedir."""
    return os.path.join(basedir, symbol.upper()) + '.csv'


def get_all_symbols(basedir):
    return sorted(map(filename_to_symbol, glob.glob(os.path.join(basedir, '*.csv'))))


def get_symbols_from_file(ticker_file):
    """Return the list of ticker symbol listed in the provided text file.

    The parsing is done to ignore blank lines or lines starting with # (comment).
    On a non-comment row, only the first word is taken as a symbol.  This allow crafting the file with
    optional description following the symbol.
    """
    ticker_list = []

    with open(ticker_file, 'r') as f:
        for ticker_row in f.readlines():
            ticker_row = ticker_row.strip() # remove leading and trailing whitespace
            if not ticker_row or ticker_row[0] == "#":  # skip comment line starting with #
                continue
            ticker = ticker_row.split()[0] # split on whitespace
            ticker_list.append(ticker)

    return ticker_list


def download_url(url):
    """Download a URL and provide the result as a big string."""
    try_again = True
    count = 0
    s = ""
    while try_again and count < 5:
        try:
            s = urllib.urlopen(url).read().strip()
            try_again = False
        except Exception:
            print("Error, will try again")
            time.sleep(0.5)  # 500 ms sleep
            count += 1
    return s


def download_data(symbol, basedir, start_date, end_date):
    """Wrapper function to yqd library."""
    print("Downloading:{} ...".format(symbol))
    symbol = symbol.upper()
    # Date 1
    d1 = "{0:0>4}".format(start_date.year) + \
         "{0:0>2}".format(start_date.month) + \
         "{0:0>2}".format(start_date.day)

    # Date 2
    d2 = "{0:0>4}".format(end_date.year) + \
         "{0:0>2}".format(end_date.month) + \
         "{0:0>2}".format(end_date.day)

    f = symbol_to_filename(symbol, basedir)

    data = yqd.load_yahoo_quote(symbol, d1, d2)
    # prevent writing invalid data
    if len(data) > 0:
        fh = open(f, 'w')
        fh.write(data)
        fh.close()


def update_all_symbols(basedir, start_date, end_date):
    """Re-download all symbols found in the basedir."""
    for s in get_all_symbols(basedir):
        download_data(s, basedir, start_date, end_date)


def normalize_data_frame(df):
    return df / df.iloc[0]


def fill_nan_data(df):
    """Fill the data in the given dataframe in place so no NaN gaps remain."""

    # print(df.loc[df.isna().any(axis=1)])
    # Data filling is done in 2 steps
    # 1. Fill forward nan with last known good value.
    df.fillna(method='ffill', inplace=True)
    # 2. Fill baward nan with first known good value.
    df.fillna(method='backfill', inplace=True)


# TBD Are these get still useful?
def get_date(df):
    return [i.date() for i in df.index]


def get_open(df):
    return df['Open'].values


def get_high(df):
    return df['High'].values


def get_low(df):
    return df['Low'].values


def get_close(df):
    return df['Close'].values


def get_volume(df):
    return df['Volume'].values


def load_data_frame(csv_file, start_date, end_date, adjust_price=True):
    try:
        print("Loading {} ...".format(filename_to_symbol(csv_file)))

        df = pd.read_csv(csv_file, index_col='Date', parse_dates=True)

        if len(df.index[df.index.duplicated()].unique()) > 0:
            raise Exception('Duplicated index in file {}'.format(csv_file))

        df.sort_index(inplace=True)

        # Re-index to only have the relevant date range
        date_range = pd.date_range(start=start_date, end=end_date, name='Date')
        df = df.reindex(date_range)

        # Discarding NaN values that are all NaN for a given row
        df.dropna(how='all', inplace=True)

        # Make sure none isolated remains:
        if df.isna().any().any():
            # To show the NaN
            print(df.loc[df.isna().all(axis=1)])
            raise Exception("ERROR {} contains isolated NaN".format(csv_file))

        if adjust_price:
            # Adjusting Columns based on Adjusted Close
            r = df['Adj Close'] / df['Close'] # ratio
            for col in ['Open', 'High', 'Low', 'Close']: # n/a for 'Volume'
                df[col] *= r
            df.drop('Adj Close', axis=1, inplace=True)

        # Axis naming
        df.rename_axis('DATA', axis='columns', inplace=True)

        return df

    except Exception as e:
        print(type(e))  # the exception instance
        print(e.args)  # arguments stored in .args
        print(e)  # __str__ allows args to be printed directly
        print('Error parsing ' + csv_file)

        return None


def validate_symbol_data(csv_file):
    """Check for basic errors in historical market data."""
    valid = True # Default
    f = open(csv_file, 'r')
    f.seek(0)
    try:
        dialect = csv.Sniffer().sniff(f.read(1024))
        if dialect:
            pass  # validation stops here
        else:  # csv was not able to find a dialect, consider not valid CSV
            valid = False
    except Exception:
        valid = False
    f.close()
    return valid
