# To make print working for Python2/3
from __future__ import print_function

import datetime
import glob
import shutil

import stock_db_mgr as sdm
import finance_utils as fu

startdate = datetime.date(2018, 1, 1)
today = datetime.date.today()

# Pick one:
# enddate = datetime.date(2018, 2, 22)
enddate = today


def list_all_stockdb():
    txt_list = glob.glob('stock_db/*.txt')
    return [i.replace('.txt', '').replace('stock_db/', '') for i in txt_list]


def check_db(path):
    print("Validating {} ...".format(path))
    # Create data base:
    db = sdm.StockDBMgr('./stock_db/' + path, startdate, enddate)

    # db.update_all_symbols()

    inv = []

    symbol_list = db.get_all_symbols()
    # print(symbol_list)

    for s in symbol_list:
        if not db.validate_symbol_data(s):
            inv.append(s)
            continue

        df = db.get_symbol_data(s)

        t = startdate
        if df is not None and len(df) > 0:
            t = df.iloc[-1].name.date()
        else:
            inv.append(s)
            continue

        if (today - t) > datetime.timedelta(4):
            inv.append(s)
            # print("%s: len = %d" % (s, len(df)))

    if len(inv) > 0:
        print("  Invalid list:")
        for s in inv:
            print("    " + s)


def get_timestamp():
    return datetime.datetime.today().strftime('%Y%m%d_%H%M%S.%f')


def find_inv_csv(db_dir, inv_dir):
    db = sdm.StockDBMgr(db_dir)
    symbol_list = db.get_all_symbols()
    for s in symbol_list:
        if not db.validate_symbol_data(s):
            inv_csv = fu.symbol_to_filename(s, db_dir)
            bak_csv = fu.symbol_to_filename(s + '_' + get_timestamp(), inv_dir)
            print("%s => %s" %(inv_csv, bak_csv))
            shutil.copy(inv_csv, bak_csv)


def analyze_inv(db_dir):
    db = sdm.StockDBMgr(db_dir, adjust_price=False)

    df = db.get_all_symbol_single_data_item('Adj Close')

    for col in db.get_symbol_data(db.get_all_symbols()[0]):
        df = db.get_all_symbol_single_data_item(col)
        print(col, df.apply(lambda c: c.eq(c.iloc[0]).all(), axis=1).all())


def _main():
    #find_inv_csv('./stock_db/test', './stock_db/test_bad')
    analyze_inv('./stock_db/test_xom')
    return

    db = list_all_stockdb()
    for p in db:
        check_db(p)


if __name__ == '__main__':
    _main()
