from copy import deepcopy
import pandas as pd
import numpy as np
import datetime
import math
import scipy as sp
import scipy.stats as sps

# user
import finance_utils as fu
import stock_db_mgr as sdm
import tmxstockquote as tsq

startdate = datetime.date(2014, 1, 6) # Start of Questrade portfolio
startdate = datetime.date(2013, 8, 12) # Start of Questrade portfolio component highest start date (VUN.TO)
today = datetime.date.today()

# Pick one:
#enddate = datetime.date(2018, 1, 1)
enddate = today


def indicator_test():
    db = sdm.CStockDBMgr('./stock_db/tsx', startdate, enddate)
    print "Loading all symbols to a panel."
    wp = db.getAllSymbolData()
    print "Loading done."

    rp = (wp.ix[:, :, "Close"].ix[-1] - wp.ix[:, :, "Close"].min()) / (wp.ix[:, :, "Close"].max() - wp.ix[:, :, "Close"].min())
    rps = 2.0 * rp - 1.0
    rr = (wp.ix[:, :, "Close"].max() - wp.ix[:, :, "Close"].min()) / wp.ix[:, :, "Close"].max()

    t = rps * rr.pow(0.1)

    # Price in the floor (5% tolerance) & 15% drop
    t.ix[(rp < 0.05) & (rr > 0.15)]

    pass

# TBD bad bad bad design... math does not work
def qt_test():
    db = sdm.CStockDBMgr('./stock_db/qt', startdate, enddate)
    print "Loading all symbols to a panel."
    wp = db.getAllSymbolData()
    print "Loading done."

    # Base ratio
    ratio = {
        'XBB.TO': 0.1,
        'ZCN.TO': 0.3,
        'VUN.TO': 0.3,
        'XEF.TO': 0.2,
        'XEC.TO': 0.1
    }

    df = wp.ix[:, :, "Close"]
    df.dropna(inplace=True)

    pf = (df * ratio).sum(axis=1)

    g1 = (pf[-1] - pf[0]) / pf[0]

    newG = g1

    keys = ratio.keys()
    keys.sort()

    for i in range(100):
        #print "Iteration ", i
        r = np.random.random(len(ratio))
        r = (r / r.sum())  # Make sure sum = 1.0

        ratio2 = dict(zip(keys, r))

        pf2 = (df * ratio2).sum(axis=1)

        g2 = (pf2[-1] - pf2[0]) / pf2[0]

        if g2 > newG:
            newRatio = deepcopy(ratio2)
            newG = g2
            print "New ratio:", newG, newRatio

    #pd.concat([pf, pf2], axis=1).plot()
    pass

def correlation_test():
    db = sdm.CStockDBMgr('./stock_db/qt', startdate, enddate)
    df = db.getAllSymbolDataSingleItem('Close')
    df.dropna(axis=1, how='any', inplace=True)
    symbols = list(df.columns)
    n = len(symbols)
    dfc = pd.DataFrame(index=symbols, data=np.zeros((n, n)), columns=symbols)

    for s1 in symbols:
        for s2 in symbols:
            c = sps.pearsonr(df.ix[:, s1], df.ix[:, s2])[0]
            dfc.ix[s1, s2] = c

    #print dfc

    # Find inverse correlation
    print dfc.min()
    print dfc.idxmin()
    pass

def _main():
    #indicator_test()
    #qt_test()
    correlation_test()

if __name__ == '__main__':
    _main()
