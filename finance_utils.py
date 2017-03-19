#-------------------------------------------------------------------------------
# Name:        finance_utils
# Purpose:
#
# Author:      temp
#
# Created:     18-03-2017
# Copyright:   (c) temp 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import glob
import urllib
import datetime


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
def downloadData(symbol, basedir, startDate, endDate):
    print "Downloading:%s" % symbol
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
def updateAllSymbols(basedir, startDate, endDate):
    for s in getAllSymbolsAvailable(basedir):
        downloadData(s, basedir, startDate, endDate)


def main():
    _defBaseDir = './stock_db/test'

    startDate = datetime.date(1900, 1, 1)
    endDate = datetime.date.today()

    s = 'SPY'

    f = symbolToFilename(s, _defBaseDir)
    print f
    print filenameToSymbol(f)

    print getAllSymbolsAvailable(_defBaseDir)
    downloadData(s, _defBaseDir, startDate, endDate)
    updateAllSymbols(_defBaseDir, startDate, endDate)
    print getSymbolsFromFile('stock_db/dj.txt')


if __name__ == '__main__':
    main()
