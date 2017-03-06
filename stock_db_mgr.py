#-------------------------------------------------------------------------------
# Name:        Stock Data Base Manager
# Purpose:
#
# Author:      Mathieu Gouin
#-------------------------------------------------------------------------------

# system
import os
import glob
import datetime
import urllib
import time

# custom
import numpy as np
from matplotlib.finance import parse_yahoo_historical

# user
import Bar


# Defaults:
_defStartDate = datetime.date(1900, 1, 1)
_defEndDate = datetime.date.today()

#-------------------------------------------------------------------------------
# Utils
def getDate(barArray):
    return np.array([b.date for b in barArray])

def getOpen(barArray):
    return np.array([b.open for b in barArray], dtype=np.float64)

def getHigh(barArray):
    return np.array([b.high for b in barArray], dtype=np.float64)

def getLow(barArray):
    return np.array([b.low for b in barArray], dtype=np.float64)

def getClose(barArray):
    return np.array([b.close for b in barArray], dtype=np.float64)

def getVolume(barArray):
    return np.array([b.volume for b in barArray], dtype=np.float64)

def filenameToSymbol(filename):
    return os.path.basename(filename).replace('.csv', '')

def symbolToFilename(symbol, basedir):
    return os.path.join(basedir, symbol.upper()) + '.csv'

def getAllSymbolsAvailable(basedir):
    return map(filenameToSymbol, glob.glob(os.path.join(basedir, '*.csv')))

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
# http://www.quantshare.com/sa-43-10-ways-to-download-historical-stock-quotes-data-for-free
def downloadData(symbol, basedir, startDate=None, endDate=None):
    print "Downloading:%s" % symbol
    if startDate == None:
        startDate = _defStartDate
    if endDate == None:
        endDate = _defEndDate
    ticker = symbol.upper()
    # Date 1
    d1 = (startDate.month-1, startDate.day, startDate.year)
    # Date 2
    d2 = (endDate.month-1, endDate.day, endDate.year)

    dividends = False # not supported for now
    if dividends:
        g='v'
    else:
        g='d'

    #   or:  'http://ichart.finance.yahoo.com/table.csv?'
    urlFmt = 'http://table.finance.yahoo.com/table.csv?a=%d&b=%d&c=%d&d=%d&e=%d&f=%d&s=%s&y=0&g=%s&ignore=.csv'

    url =  urlFmt % (d1[0], d1[1], d1[2], d2[0], d2[1], d2[2], ticker, g)

    cachename = symbolToFilename(symbol, basedir)

    fh = open(cachename, 'w')
    fh.write(downloadUrl(url))
    fh.close()

#-------------------------------------------------------------------------------
def updateAllSymbols(basedir, startDate=None, endDate=None):
    if startDate == None:
        startDate = _defStartDate
    if endDate == None:
        endDate = _defEndDate
    for s in getAllSymbolsAvailable(basedir):
        downloadData(s, basedir, startDate, endDate)

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
# Check for basic errors in historical market data
def validateData(csvFile):
    print "Validating:%s" % csvFile
    valid = True # Default
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
    f.close()
    return valid

#-------------------------------------------------------------------------------
def getSymbolData(symbol, basedir, startDate=None, endDate=None):
    if startDate == None:
        startDate = _defStartDate
    if endDate == None:
        endDate = _defEndDate
    f = symbolToFilename(symbol, basedir)
    if (not os.path.exists(f)):
        downloadData(symbol, basedir, startDate, endDate)
    # if data is already there, assume it is up to date (to save repetive download)

    # TBD to check which is faster...
    if True:  # default
        return loadData(f, startDate, endDate)
    else:
        # This method does not support date range
        print "Loading:%s" % symbol
        fh = open(f, 'r')
        d = parse_yahoo_historical(fh, adjusted=True, asobject=True)
        fh.close()
        return d

#-------------------------------------------------------------------------------
class CStockDBMgr:
    def __init__(self, basedir, startDate=None, endDate=None):
        if startDate == None:
            startDate = _defStartDate
        if endDate == None:
            endDate = _defEndDate
        self.basedir   = basedir
        self.startDate = startDate
        self.endDate   = endDate

    def getAllSymbolsAvailable(self):
        return getAllSymbolsAvailable(self.basedir)

    def downloadData(self, symbol):
        downloadData(symbol, self.basedir, self.startDate, self.endDate)

    def updateAllSymbols(self):
        updateAllSymbols(self.basedir, self.startDate, self.endDate)

    def getSymbolData(self, symbol, startDate=None, endDate=None):
        if startDate == None:
            startDate = self.startDate
        if endDate == None:
            endDate = self.endDate
        return getSymbolData(symbol, self.basedir, startDate, endDate)

    def validateSymbolData(self, symbol):
        return validateData(symbolToFilename(symbol, self.basedir))

#-------------------------------------------------------------------------------
def _main():
    sdm = CStockDBMgr('./stock_db/qt')
    symbolList = sdm.getAllSymbolsAvailable()
    print symbolList
    sdm.validateSymbolData(symbolList[0])
    d = sdm.getSymbolData(symbolList[0])
    print d[0].toString()
    print getDate(d)[0]
    print getOpen(d)[0]
    print getHigh(d)[0]
    print getLow(d)[0]
    print getClose(d)[0]
    print getVolume(d)[0]

    #sdm.updateAllSymbols()
    t0 = time.clock()
    for s in sdm.getAllSymbolsAvailable():
        print sdm.validateSymbolData(s)
    dt = time.clock() - t0
    print dt

    t0 = time.clock()
    for s in sdm.getAllSymbolsAvailable():
        d = sdm.getSymbolData(s)
    dt = time.clock() - t0
    print dt
    return

    _defBaseDir = './stock_db/test'
    s = 'CP.TO'
    f = symbolToFilename(s, _defBaseDir)
    print f
    print filenameToSymbol(f)
    print getAllSymbolsAvailable(_defBaseDir)
    downloadData(s, _defBaseDir)
    d = getSymbolData(s, _defBaseDir)
    updateAllSymbols(_defBaseDir)
    print getSymbolsFromFile('stock_db/dj.txt')

if __name__ == '__main__':
    _main()
