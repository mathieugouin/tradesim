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
import os

# custom
import numpy as np
#from matplotlib.finance import parse_yahoo_historical
import pandas as pd

# user
import Bar
import finance_utils as fu


# Defaults:
_defStartDate = datetime.date(1900, 1, 1)
_defEndDate = datetime.date.today()

#-------------------------------------------------------------------------------
# Utils
def getDate(df):
    #return df.index.values
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
    # Default dates handling
    if startDate is None:
        startDate = _defStartDate
    if endDate is None:
        endDate = _defEndDate

    f = fu.symbolToFilename(symbol, basedir)
    if (not os.path.exists(f)):
        fu.downloadData(symbol, basedir, startDate, endDate)
    # if data is already there, assume it is up to date (to save repetitive download)

    df = fu.loadDataFrame(f, startDate, endDate)
    return df

#-------------------------------------------------------------------------------
class CStockDBMgr:
    def __init__(self, basedir, startDate=None, endDate=None):
        if startDate is None:
            startDate = _defStartDate
        if endDate is None:
            endDate = _defEndDate
        self.basedir   = basedir
        self.startDate = startDate
        self.endDate   = endDate
        self.wp        = None
        self.dataDic   = None

    def getAllSymbolsAvailable(self):
        return fu.getAllSymbolsAvailable(self.basedir)

    def downloadData(self, symbol):
        fu.downloadData(symbol, self.basedir, self.startDate, self.endDate)

    def updateAllSymbols(self):
        fu.updateAllSymbols(self.basedir, self.startDate, self.endDate)

    def getSymbolData(self, symbol, startDate=None, endDate=None):
        if startDate is None:
            startDate = self.startDate
        if endDate is None:
            endDate = self.endDate
        return getSymbolData(symbol, self.basedir, startDate, endDate)

    # TBD Remove date args for this class...
    def getAllSymbolDataDic(self):
        # Load it once
        if self.dataDic is None:
            t0 = time.clock()
            self.dataDic = {}
            for s in self.getAllSymbolsAvailable():
                print "Loading " + s + " ..."
                df = self.getSymbolData(s, self.startDate, self.endDate)
                #print df.shape[0]
                self.dataDic[s] = df
            dt = time.clock() - t0
            print "Load time:", dt

            noneKeys = [k for k in self.dataDic.keys() if self.dataDic[k] is None]
            for k in noneKeys:
                print "Removing {} as it contains error".format(k)
                del self.dataDic[k]

        return self.dataDic

    def getAllSymbolData(self, startDate=None, endDate=None):
        # Load it once
        if self.wp is None:
            t0 = time.clock()
            dic = self.getAllSymbolDataDic()
            dt = time.clock() - t0
            self.wp = pd.Panel(dic)
            print "Load time:", dt

        return self.wp


    def validateSymbolData(self, symbol):
        return validateSymbolData(fu.symbolToFilename(symbol, self.basedir))

#-------------------------------------------------------------------------------
def _main():
    db = CStockDBMgr('./stock_db/qt', datetime.date(2017, 1, 1), datetime.date(2018, 1, 1))
    #db = CStockDBMgr('./stock_db/test')
    #db.updateAllSymbols()
    symbolList = db.getAllSymbolsAvailable()
    print symbolList

    # Do with only first symbol
    s = symbolList[0]
    print s, 'Valid', db.validateSymbolData(s)
    d = db.getSymbolData(s)

    if False:
        print getDate(d)[0]
        print getOpen(d)[0]
        print getHigh(d)[0]
        print getLow(d)[0]
        print getClose(d)[0]
        print getVolume(d)[0]

    if False:
        print "Validating symbols"
        t0 = time.clock()
        for s in db.getAllSymbolsAvailable():
            if not db.validateSymbolData(s):
                print s, " failed validation"
        dt = time.clock() - t0
        print dt

    if True:
        print "Loading all symbols to a panel"
        wp = db.getAllSymbolData()
        print wp


if __name__ == '__main__':
    _main()
