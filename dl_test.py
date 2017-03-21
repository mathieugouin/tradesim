import datetime
import stock_db_mgr as sdm

import gstockquote as gsq
import ystockquote as ysq

startdate = datetime.date(1900, 1, 1)
today = enddate = datetime.date.today()

tickerfile = './stock_db/tsx.txt'
#tickerfile = './stock_db/qt.txt'

# Create data base:
db = sdm.CStockDBMgr('./stock_db/tsx')
#db = sdm.CStockDBMgr('./stock_db/sp500')
#db = sdm.CStockDBMgr('./stock_db/test')

#db.updateAllSymbols()

inv = []

symbolList = db.getAllSymbolsAvailable()
print len(symbolList)

for s in symbolList:
    print s #, ysq.get_dividend_yield(s), ysq.get_name(s)

    if not db.validateSymbolData(s):
        inv.append(s)
        continue

    # Only applies if recent download...
    if False:
        #db.downloadData(s)
        r = db.getSymbolData(s)

        t = startdate
        if len(r) > 0:
            #t = r[-1].date
            t = r.ix[-1].name.date()
        else:
            inv.append(s)
            continue

        #gsq.get_company_name(s)
        #t = float(ysq.get_price(s))
        #print "%s: %s" % (s, t)

        if (today - t) > datetime.timedelta(4):
            inv.append(s)
            print "%s: len = %d" %(s, len(r))

print "Invalid list:"
for s in inv:
    print s
