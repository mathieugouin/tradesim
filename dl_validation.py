# To make print working for Python2/3
from __future__ import print_function

import datetime
import glob

import stock_db_mgr as sdm
import ystockquote as sq

startdate = datetime.date(1900, 1, 1)
today = datetime.date.today()

# Pick one:
# enddate = datetime.date(2018, 2, 22)
enddate = today


def list_all_stockdb():
    txt_list = glob.glob('stock_db/*.txt')
    return [i.replace('.txt', '').replace('stock_db/', '') for i in txt_list]


def check_db(path):
    # Create data base:
    db = sdm.StockDBMgr('./stock_db/' + path, startdate, enddate)

    # db.update_all_symbols()

    inv = []

    symbolList = db.get_all_symbols()
    print(len(symbolList))
    print(symbolList)

    for s in symbolList:
        if False:
            print("symbol:{}, yield:{}, name:{}".format(s, sq.get_dividend_yield(s), sq.get_name(s)))

        if not db.validate_symbol_data(s):
            inv.append(s)
            continue

        # Only applies if recent download...
        if True:
            df = db.get_symbol_data(s)

            t = startdate
            if df is not None and len(df) > 0:
                # t = r[-1].date
                t = df.iloc[-1].name.date()
            else:
                inv.append(s)
                continue

            if (today - t) > datetime.timedelta(4):
                inv.append(s)
                print("%s: len = %d" % (s, len(df)))

    print("Invalid list:")
    for s in inv:
        print(s)


def _main():
    dbs = list_all_stockdb()
    for p in dbs:
        check_db(p)


if __name__ == '__main__':
    _main()
