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

#-------------------------------------------------------------------------------
# Wrapper to yqd
def downloadData(symbol, basedir, startDate, endDate):
    print "Downloading:%s" % symbol
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

#-------------------------------------------------------------------------------
def updateAllSymbols(basedir, startDate, endDate):
    for s in getAllSymbolsAvailable(basedir):
        downloadData(s, basedir, startDate, endDate)


#-------------------------------------------------------------------------------
def loadDataFrame(csvFile, startDate, endDate):
    try:
        df = pd.read_csv(csvFile, index_col='Date', parse_dates=True)

        if len(df.index.get_duplicates()) > 0:
            raise Exception('Duplicated index in file {}'.format(csvFile))

        df.sort_index(inplace=True)

        # Re-index to only have the relevant date range
        dateRange = pd.date_range(startDate, endDate)
        df = df.reindex(dateRange)

        # Discarding NaN values that are all NaN for a given row
        df.dropna(how='all', inplace=True)

        # Make sure none isolated remains:
        if df.isna().any().any():
            print "ERROR ", csvFile, "contains isolated NaN"

        # to show the NaN
        #df.loc[df.isna().all(axis=1)]

        # Adjusting Columns based on Adjusted Close
        r = df['Adj Close'] / df['Close'] # ratio
        for col in ['Open', 'High', 'Low', 'Close']:
            df[col] *= r

        df.drop('Adj Close', axis=1, inplace=True)

        return df
    except:
        print 'Error parsing ' + csvFile
        return None


#-------------------------------------------------------------------------------
# TBD: currently only error print when incorrect data...
def loadData(csvFile, startDate, endDate):
    print "Loading:%s" % csvFile
    bars = [] # array
    # The CSV files are downloaded from yahoo historical data
    f = open(csvFile, 'r')
    #lineSplit  0,   1,   2,   3,  4,    5,     6
    #priceData       0,   1,   2,  3,    4,     5
    #           Date,Open,High,Low,Close,Volume,Adj Close
    #           2012-03-21,204.32,205.77,204.30,204.69,3329900,204.69
    f.seek(0)
    f.readline() # skip header row
    for l in f.readlines():
        # Date,Open,High,Low,Close,Volume,Adj Close
        lineSplit = l.strip().split(',')
        if len(lineSplit) != 7:
            print "Error: Invalid line, missing data"
            continue
        dateSplit = map(int, lineSplit[0].split('-'))
        date = datetime.date(dateSplit[0], dateSplit[1], dateSplit[2])
        # Yahoo CSV data is most recent first
        if date < startDate: # Data starting with this line in the file is too old
            break # stop processing this file
        if startDate <= date and date <= endDate:
            priceData = map(float, lineSplit[1:])
            if priceData[3] != 0:
                adjRatio = priceData[5] / priceData[3] # Adj Close / Close
            else:
                adjRatio = 1.0
                print "Error: Invalid line, close price = 0"
                continue

            # Create new Bar data
            bar = Bar.CBar(
                        date,
                        priceData[0] * adjRatio, # open
                        priceData[1] * adjRatio, # high
                        priceData[2] * adjRatio, # low
                        priceData[3] * adjRatio, # close
                        priceData[4]             # volume (in nb of shares)
                    )
            # Add to the list
            bars.append(bar)
    f.close()
    bars.reverse() # now bars[0] is the earliest
    return bars


#-------------------------------------------------------------------------------
def main():
    dir = './stock_db/test'

    startDate = datetime.date(1900, 1, 1)
    endDate = datetime.date.today()

    s = 'SPY'

    f = symbolToFilename(s, dir)
    print f
    print filenameToSymbol(f)

    print getAllSymbolsAvailable(dir)
    downloadData(s, dir, startDate, endDate)
    updateAllSymbols(dir, startDate, endDate)
    print getSymbolsFromFile('stock_db/dj.txt')
    df = loadDataFrame(f, datetime.date(2018, 1, 1), datetime.date(2018, 2, 1))
    print df.describe()
    df = loadDataFrame(f, startDate, endDate)
    print df.describe()


if __name__ == '__main__':
    main()
