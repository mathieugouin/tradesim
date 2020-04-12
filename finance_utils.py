"""Finance utilities library."""

# To make print working for Python2/3
from __future__ import print_function

# System
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
    return os.path.basename(filename).replace('.csv', '')


def symbol_to_filename(symbol, basedir):
    return os.path.join(basedir, symbol.upper()) + '.csv'


# TBD available in the name to remove?
def get_all_symbols_available(basedir):
    return sorted(map(filename_to_symbol, glob.glob(os.path.join(basedir, '*.csv'))))


def get_symbols_from_file(ticker_file):
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
    for s in get_all_symbols_available(basedir):
        download_data(s, basedir, start_date, end_date)


def normalize_data_frame(df):
    return df / df.iloc[0]


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

        if len(df.index.get_duplicates()) > 0:
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


def validateSymbolData(csvFile):
    """Check for basic errors in historical market data."""
    #print("Validating:%s" % csvFile)
    valid = True # Default
    # The CSV files are downloaded from yahoo historical data
    f = open(csvFile, 'r')
    #lineSplit  0,   1,   2,   3,  4,    5,     6
    #priceData       0,   1,   2,  3,    4,     5
    #           Date,Open,High,Low,Close,Volume,Adj Close
    #           2012-03-21,204.32,205.77,204.30,204.69,3329900,204.69
    f.seek(0)
    try:
        dialect = csv.Sniffer().sniff(f.read(1024))
        if dialect:
            if False: # temp for now, csv only...
                f.seek(0)
                f.readline() # skip header row
                for l in f.readlines():
                    # Date,Open,High,Low,Close,Volume,Adj Close
                    lineSplit = l.strip().split(',')
                    if len(lineSplit) != 7:
                        print("Error: Invalid line, missing data")
                        valid = False
                        break
                    dateSplit = map(int, lineSplit[0].split('-'))
                    if len(dateSplit) != 3:
                        print("Error: Invalid date format")
                        valid = False
                        break
                    priceData = map(float, lineSplit[1:])
                    if priceData[3] == 0 or priceData[5] == 0:
                        print("Error: Invalid price data")
                        valid = False
                        break
        else: # csv was not able to find a dialect, consider not valid CSV
            valid = False
    except Exception:
        valid = False
    f.close()
    return valid


def _main():
    sf = 'stock_db/dj.txt'
    print("symbol file {} contains the following stocks: {}".format(sf, get_symbols_from_file(sf)))

    d = './stock_db/test'

    s = 'SPY'
    f = symbol_to_filename(s, d)
    print("symbol {} with directory {} gives filename {}".format(s, d, f))
    print("filename {} gives symbol {}".format(f, filename_to_symbol(f)))
    print("validateSymbolData {} = {}".format(f, validateSymbolData(f)))

    print("directory {} contains the following stocks: {}".format(d, get_all_symbols_available(d)))

    start_date = datetime.date(1900, 1, 1)
    end_date = datetime.date.today()

    if False:
        download_data(s, d, start_date, end_date)
        update_all_symbols(d, start_date, end_date)
    df = load_data_frame(f, datetime.date(2018, 1, 1), datetime.date(2018, 4, 1))
    print(df.describe())
    print(df.head())

    print(get_date(df)[0:3])
    print(get_open(df)[0:3])
    print(get_high(df)[0:3])
    print(get_low(df)[0:3])
    print(get_close(df)[0:3])
    print(get_volume(df)[0:3])

    # Not applicable for a single stock, but just to test...
    print(normalize_data_frame(df).head())

    print(download_url("https://www.google.ca")[0:100])


if __name__ == '__main__':
    _main()
