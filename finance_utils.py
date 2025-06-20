"""Finance utilities library."""

# System
import re
import os
import glob
import csv
import math
# For socket timeout
import socket
# Use six to import urllib so it is working for Python2/3
from six.moves import urllib

# Custom
import pandas as pd

# User
import yqd


def calc_commission(nb_share):
    """Return the regular stock commission on Questrade: positive=Buy, negative=Sell."""
    # 0.01 $ per share (min 4.95, max 9.95)
    # 0.0035 $ per share ECN fees (sometimes waived, but simpler to always include them)
    nb_share = math.fabs(nb_share)
    return (nb_share > 0) * (nb_share * 0.0035 + min(9.95, max(0.01 * nb_share, 4.95)))


def calc_commission_etf(nb_share):
    """Return the ETF trade commission on Questrade: positive=Buy, negative=Sell."""
    # Sell only: 0.01 $ per share (min 4.95, max 9.95)
    # Buy or sell: 0.0035 $ per share ECN fees
    #   (sometimes waived, but simpler to always include them)
    return (nb_share < 0) * min(9.95, max(4.95, -nb_share * 0.01)) + math.fabs(nb_share) * 0.0035


def filename_to_symbol(filename):
    """Return the basename of the filename without the .csv at the end."""
    return re.sub(r'\.csv', '', re.sub('^_', '^', os.path.basename(filename)), flags=re.IGNORECASE)


def symbol_to_filename(symbol, basedir):
    """Return the complete filename path based on the symbol and basedir."""
    return os.path.join(basedir, re.sub(r'^\^', '_', symbol.upper())) + '.csv'


def get_all_symbols(basedir):
    """Return a sorted list of symbols available in a basedir folder.

    The symbol list is based on the presence of a *.csv file in the basedir.
    """
    return sorted(map(filename_to_symbol, glob.glob(os.path.join(basedir, '*.csv'))))


def get_symbols_from_file(ticker_file):
    """Return the list of ticker symbol listed in the provided text file.

    The parsing is done to ignore blank lines or lines starting with # (comment).
    On a non-comment row, only the first word is taken as a symbol.
    This allow crafting the file with optional description following the symbol.
    """
    ticker_list = []

    with open(ticker_file, 'r') as f:
        for ticker_row in f.readlines():
            ticker_row = ticker_row.strip()  # remove leading and trailing whitespace
            if not ticker_row or ticker_row[0] == "#":  # skip comment line starting with #
                continue
            ticker = ticker_row.split()[0]  # split on whitespace
            ticker_list.append(ticker)

    return ticker_list


def download_url(url):
    """Download a URL and provide the result as a single string."""
    # Headers to fake a user agent
    headers = {
        'User-Agent':   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                        '(KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
    }

    s = ""
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as f:
            charset = f.info().get_content_charset()

            if charset is None:  # Default according to HTTP
                charset = 'iso-8859-1'

            r = f.read()
            s = r.decode(charset)

    except (socket.timeout, urllib.error.HTTPError, urllib.error.URLError) as e:
        print("URLError: {}".format(e))
    return s


def download_data(symbol, basedir, start_date, end_date):
    """Wrapper function to yqd library."""
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

    yqd.load_yahoo_quote(symbol, d1, d2, f)


def update_all_symbols(basedir, start_date, end_date):
    """Re-download all symbols found in the basedir."""
    for s in get_all_symbols(basedir):
        download_data(s, basedir, start_date, end_date)


def clean_dataframe(df, start_date):
    """Return a DataFrame with symbols 'mostly' valid from start_date.

    Explaining 'mostly':
    * Symbols with at least one valid day in the first 5 days from start_date.
      This is to prevent symbols that are too young and were not present at start_date.

    * Symbols with at least one valid day in the last 5 days from the end of the DataFrame.
      This is to prevent symbols that stopped trading before the end of the DataFrame.
    """
    nb_days = 5  # valid grace period from start and end date

    valid_symbols_at_start = df.loc[start_date:].iloc[0:nb_days].notna().any().pipe(lambda x: x[x]).index
    valid_symbols_at_end = df.iloc[-nb_days:].notna().any().pipe(lambda x: x[x]).index

    return df.loc[start_date:][valid_symbols_at_start.intersection(valid_symbols_at_end)]


def fill_nan_data(df, inplace=False):
    """Fill the data in the given DataFrame so no NaN gaps remain.

    This is done by:
    1. Fill forward nan with last known good value.
    2. Fill backward nan with first known good value.
    Returns: DataFrame with missing values filled or None if inplace=True.
    """
    # Data filling is done in 2 steps
    if inplace:
        # 1. Fill forward nan with last known good value.
        df.ffill(inplace=inplace)
        # 2. Fill backward nan with first known good value.
        df.bfill(inplace=inplace)
        return None

    # 1. Fill forward nan with last known good value.
    df2 = df.ffill(inplace=inplace)
    # 2. Fill backward nan with first known good value.
    df2 = df2.bfill(inplace=inplace)
    return df2


def normalize_dataframe(df):
    """Return a new DataFrame normalized so that first row is all 1.0."""
    return df / df.iloc[0]


def load_dataframe(csv_file, start_date, end_date):
    """Load a CSV stock data file into a pandas DataFrame.

    The DataFrame is sorted chronologically by date.
    If requested, the prices (open, high, low, close) are adjusted according
    to the adjusted close price.
    """
    try:
        df = pd.read_csv(csv_file, index_col='Date', parse_dates=True)

        # Make sure no duplicated dates:
        if df.index.duplicated().any():
            raise AssertionError('Duplicated index in file {}'.format(csv_file))

        df.sort_index(inplace=True)

        # Keep only the required date range
        df = df.loc[start_date:end_date]

        # Discarding NaN values that are all NaN for a given row
        df.dropna(how='all', inplace=True)

        # Make sure none isolated remains:
        if df.isna().any().any():
            # To show the NaN
            print(df.loc[df.isna().all(axis='columns')])
            raise AssertionError("ERROR {} contains isolated NaN".format(csv_file))

        # Axis naming matching the symbol name
        df.rename_axis(filename_to_symbol(csv_file), axis='columns', inplace=True)

        return df

    except Exception as e:
        print(type(e))  # the exception instance
        print(e.args)  # arguments stored in .args
        print(e)  # __str__ allows args to be printed directly
        print('Error parsing ' + csv_file)

        return None


def validate_dataframe(df):
    """Check for basic errors in historical data.  Return True when valid, False otherwise."""
    required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    for column in required_columns:
        if column not in df:
            return False

    if len(df.columns) > len(required_columns) + 1:
        return False

    # "Adj Close" is optionnal and only present when DataFrame is not adjusted.
    if len(df.columns) == len(required_columns) + 1 and "Adj Close" not in df:
        return False

    check = True

    # Compare with High
    if (df['High'] < df['Open']).any():
        check = False
    if (df['High'] < df['Low']).any():
        check = False
    if (df['High'] < df['Close']).any():
        check = False

    # Compare with Low
    if (df['Low'] > df['Open']).any():
        check = False
    if (df['Low'] > df['Close']).any():
        check = False

    return check


def validate_symbol_data_file(csv_file):
    """Check for basic errors in CSV file.  Return True when valid, False otherwise."""
    valid = False  # Default
    try:
        with open(csv_file, 'r') as f:
            f.seek(0)
            valid = csv.Sniffer().has_header(f.read(1024))
    except Exception:
        valid = False

    return valid
