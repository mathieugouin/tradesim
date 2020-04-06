from copy import deepcopy
import pandas as pd
import numpy as np
import datetime
import scipy.stats as sps

# user
import stock_db_mgr as sdm

startdate = datetime.date(2014, 1, 6) # Start of Questrade portfolio
#startdate = datetime.date(2013, 8, 12) # Start of Questrade portfolio component highest start date (VUN.TO)
today = datetime.date.today()

# Pick one:
enddate = datetime.date(2018, 1, 1)
#enddate = today


def indicator_test():
    db = sdm.CStockDBMgr('./stock_db/tsx', startdate, enddate)
    print "Loading all symbols..."
    df = db.getAllSymbolDataSingleItem('Close')
    print "Loading done."

    rp = (df.iloc[-1] - df.min()) / (df.max() - df.min())
    rps = 2.0 * rp - 1.0
    rr = (df.max() - df.min()) / df.max()

    t = rps * rr.pow(0.1)

    # Price in the floor (5% tolerance) & 15% drop
    print t.loc[(rp < 0.05) & (rr > 0.15)]


def correlation_test():
    db = sdm.CStockDBMgr('./stock_db/qt', startdate, enddate)
    df = db.getAllSymbolDataSingleItem('Close')
    df.dropna(axis=1, how='any', inplace=True)
    symbols = list(df.columns)
    n = len(symbols)
    dfc = pd.DataFrame(index=symbols, data=np.zeros((n, n)), columns=symbols)

    for s1 in symbols:
        for s2 in symbols:
            c = sps.pearsonr(df.loc[:, s1], df.loc[:, s2])[0]
            dfc.loc[s1, s2] = c

    #print dfc

    # Find inverse correlation
    print dfc.min()
    print dfc.idxmin()
    pass


def _main():
    indicator_test()
    correlation_test()


if __name__ == '__main__':
    _main()
