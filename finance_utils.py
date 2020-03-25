#-------------------------------------------------------------------------------
# Name:        finance_utils
# Purpose:     Finance utilities library.
# Author:      mgouin
#-------------------------------------------------------------------------------

# System
import os
import glob
import urllib
import datetime
import csv

# Custom
import pandas as pd

# User
import yqd
import Bar


def filenameToSymbol(filename):
    return os.path.basename(filename).replace('.csv', '')


def symbolToFilename(symbol, basedir):
    return os.path.join(basedir, symbol.upper()) + '.csv'


def getAllSymbolsAvailable(basedir):
    return sorted(map(filenameToSymbol, glob.glob(os.path.join(basedir, '*.csv'))))


def getSymbolsFromFile(tickerFile):
    tickerList = []
    try:
        f = open(tickerFile, 'r')
        for tickerRow in f.readlines():
            tickerRow = tickerRow.strip() # remove leading and trailing whitespace
            if not tickerRow or tickerRow[0] == "#":  # skip comment line starting with #
                continue
            ticker = tickerRow.split()[0] # split on whitespace
            tickerList.append(ticker)
        f.close()
    except:
        print "Error: ticker file %s not found" % tickerFile
    return tickerList


def downloadUrl(url):
    tryAgain = True
    count = 0
    s = ""
    while tryAgain and count < 5:
        try:
            s = urllib.urlopen(url).read()
            tryAgain = False
        except:
            print "Error, will try again"
            count += 1
    return s


def downloadData(symbol, basedir, startDate, endDate):
    """This is a wrapper to yqd library."""
    print "Downloading:{} ...".format(symbol)
    symbol = symbol.upper()
    # Date 1
    d1 = "{0:0>4}".format(startDate.year) + \
         "{0:0>2}".format(startDate.month) + \
         "{0:0>2}".format(startDate.day)

    # Date 2
    d2 = "{0:0>4}".format(endDate.year) + \
         "{0:0>2}".format(endDate.month) + \
         "{0:0>2}".format(endDate.day)

    f = symbolToFilename(symbol, basedir)

    data = yqd.load_yahoo_quote(symbol, d1, d2)
    # prevent writing invalid data
    if len(data) > 0:
        fh = open(f, 'w')
        fh.write(data)
        fh.close()


def updateAllSymbols(basedir, startDate, endDate):
    for s in getAllSymbolsAvailable(basedir):
        downloadData(s, basedir, startDate, endDate)


def normalizeDataFrame(df):
    return df / df.iloc[0]


def getDate(df):
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


def loadDataFrame(csvFile, startDate, endDate, adjustPrice=True):
    try:
        df = pd.read_csv(csvFile, index_col='Date', parse_dates=True)

        if len(df.index.get_duplicates()) > 0:
            raise Exception('Duplicated index in file {}'.format(csvFile))

        df.sort_index(inplace=True)

        # Re-index to only have the relevant date range
        date_range = pd.date_range(start=startDate, end=endDate, name='Date')
        df = df.reindex(date_range)

        # Discarding NaN values that are all NaN for a given row
        df.dropna(how='all', inplace=True)

        # Make sure none isolated remains:
        if df.isna().any().any():
            # To show the NaN
            print df.loc[df.isna().all(axis=1)]
            raise Exception("ERROR {} contains isolated NaN".format(csvFile))

        if adjustPrice:
            # Adjusting Columns based on Adjusted Close
            r = df['Adj Close'] / df['Close'] # ratio
            for col in ['Open', 'High', 'Low', 'Close']: # n/a for 'Volume'
                df[col] *= r
            df.drop('Adj Close', axis=1, inplace=True)

        # Axis naming
        df.rename_axis('DATA', axis='columns', inplace=True)

        return df

    except Exception as inst:
        print type(inst)    # the exception instance
        print inst.args     # arguments stored in .args
        print inst          # __str__ allows args to be printed directly,
                            # but may be overridden in exception subclasses
        print 'Error parsing ' + csvFile

        return None


def validateSymbolData(csvFile):
    """Check for basic errors in historical market data"""
    #print "Validating:%s" % csvFile
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
                        print "Error: Invalid line, missing data"
                        valid = False
                        break
                    dateSplit = map(int, lineSplit[0].split('-'))
                    if len(dateSplit) != 3:
                        print "Error: Invalid date format"
                        valid = False
                        break
                    priceData = map(float, lineSplit[1:])
                    if priceData[3] == 0 or priceData[5] == 0:
                        print "Error: Invalid price data"
                        valid = False
                        break
        else: # csv was not able to find a dialect, consider not valid CSV
            valid = False
    except:
        valid = False
    f.close()
    return valid


def _main():
    sf = 'stock_db/dj.txt'
    print "Symbol file {} contains the following stocks: {}".format(sf, getSymbolsFromFile(sf))

    dir = './stock_db/test'

    s = 'SPY'
    f = symbolToFilename(s, dir)
    print f
    print filenameToSymbol(f)

    print "Directory {} contains the following stocks: {}".format(dir, getAllSymbolsAvailable(dir))

    startDate = datetime.date(1900, 1, 1)
    endDate = datetime.date.today()

    if False:
        downloadData(s, dir, startDate, endDate)
        updateAllSymbols(dir, startDate, endDate)
    df = loadDataFrame(f, datetime.date(2018, 1, 1), datetime.date(2018, 4, 1))
    print df.describe()

    print getDate(df)[0:3]
    print getOpen(df)[0:3]
    print getHigh(df)[0:3]
    print getLow(df)[0:3]
    print getClose(df)[0:3]
    print getVolume(df)[0:3]

    df = loadDataFrame(f, startDate, endDate)
    print df.describe()

    # Not for single stock, but just to test...
    print normalizeDataFrame(df).head()


if __name__ == '__main__':
    _main()
