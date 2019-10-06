import datetime
import stock_db_mgr as sdm

#import gstockquote as gsq
#import ystockquote as ysq
import tmxstockquote as tsq

startdate = datetime.date(1900, 1, 1)
today = datetime.date.today()

# Pick one:
#enddate = datetime.date(2018, 2, 22)
enddate = today

tickerfile = './stock_db/tsx.txt'
#tickerfile = './stock_db/qt.txt'

# Create data base:
#db = sdm.CStockDBMgr('./stock_db/qt', startdate, enddate)
db = sdm.CStockDBMgr('./stock_db/tsx')
#db = sdm.CStockDBMgr('./stock_db/sp500')
#db = sdm.CStockDBMgr('./stock_db/test')

#db.updateAllSymbols()

inv = []

symbolList = db.getAllSymbolsAvailable()
print len(symbolList)
print symbolList

for s in symbolList:
    print s #, ysq.get_dividend_yield(s), ysq.get_name(s)
    print tsq.relative_range(s), tsq.test_indicator(s)

    if not db.validateSymbolData(s):
        inv.append(s)
        continue

    # Only applies if recent download...
    if False:
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
