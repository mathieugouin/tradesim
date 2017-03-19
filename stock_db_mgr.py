#-------------------------------------------------------------------------------
# Name:        Stock Data Base Manager
# Purpose:
#
# Author:      Mathieu Gouin
#-------------------------------------------------------------------------------

# system
import datetime
import time
import csv

# custom
import numpy as np
#from matplotlib.finance import parse_yahoo_historical
import pandas as pd

# user
import Bar
from finance_utils import *


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

#-------------------------------------------------------------------------------
# TBD: Date range not supported yet...
def loadDataFrame(csvFile, startDate, endDate):
    try:
        df = pd.read_csv(csvFile, index_col='Date', parse_dates=True, na_values=['nan', 'NaN', 'NAN'])
        df.sort_index(inplace=True)

        # Adjusting Columns based on Adjusted Close
        r = df['Adj Close'] / df['Close'] # ratio
        for col in ['Open', 'High', 'Low', 'Close']:
            df[col] *= r

        df.drop('Adj Close', axis=1, inplace=True)

        return df
    except:
        print 'Error parsing ' + csvFile

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
def validateSymbolData(csvFile):
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

    # Case 1
    #return loadData(f, startDate, endDate)

    # Case 2
    # This method does not support date range
    #print "Loading:%s" % symbol
    #fh = open(f, 'r')
    #d = parse_yahoo_historical(fh, adjusted=True, asobject=True)
    #fh.close()
    #return d

    # Case 3
    df = loadDataFrame(f, startDate, endDate)
    return df

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
        return validateSymbolData(symbolToFilename(symbol, self.basedir))

#-------------------------------------------------------------------------------
def _main():
    #db = CStockDBMgr('./stock_db/tsx')
    db = CStockDBMgr('./stock_db/test')
    #db.updateAllSymbols()
    symbolList = db.getAllSymbolsAvailable()
    print symbolList

    # Do with only first symbol
    s = symbolList[0]
    print db.validateSymbolData(s)
    d = db.getSymbolData(s)

    if False:
        print d[0].toString()
        print getDate(d)[0]
        print getOpen(d)[0]
        print getHigh(d)[0]
        print getLow(d)[0]
        print getClose(d)[0]
        print getVolume(d)[0]

    if True:
        print "Validating symbols"
        t0 = time.clock()
        for s in db.getAllSymbolsAvailable():
            print db.validateSymbolData(s)
        dt = time.clock() - t0
        print dt

    if True:
        print "Loading symbols to a panel"
        t0 = time.clock()
        d = {}
        for s in db.getAllSymbolsAvailable():
            df = db.getSymbolData(s)
            print len(df['Close'])
            d[s] = df
        dt = time.clock() - t0
        print dt

        wp = pd.Panel(d)
        print wp

    return

    # -----------------
    d = getSymbolData(s, _defBaseDir)

if __name__ == '__main__':
    _main()
