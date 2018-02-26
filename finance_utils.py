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

# User
import yqd

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
# Wrapper to yqd
def downloadData(symbol, basedir, startDate, endDate):
    print "Downloading:%s" % symbol
    ticker = symbol.upper()
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


if __name__ == '__main__':
    main()
