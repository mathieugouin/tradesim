# To make print working for Python2/3
from __future__ import print_function

import datetime

import parent_import
import stock_db_mgr as sdm


def _main():
    #db = sdm.StockDBMgr('../stock_db/test', datetime.date(2017, 1, 1), datetime.date(2018, 1, 1))
    #db = sdm.StockDBMgr('stock_db/tsx', datetime.date(2023, 1, 1), datetime.date(2023, 6, 1))
    db = sdm.StockDBMgr('stock_db/tsx')
    #db = sdm.StockDBMgr('../stock_db/sp500')

    symbol_list = db.get_all_symbols()
    #print(symbol_list)

    # Work with first symbol only
    s = symbol_list[0]

    if False:
        # To test caching
        df = db.get_symbol_data(s)
        df = db.get_symbol_data(s)
        db.download_data(s)
        df = db.get_symbol_data(s)
        db.update_all_symbols()
        df = db.get_symbol_data(s)

    if False:
        print("Validating symbols")
        for s in db.get_all_symbols():
            if not db.validate_symbol_data(s):
                print("{} failed validation".format(s))

    if False:
        print("Loading all symbols to a dict")
        # To test caching
        dd = db.get_all_symbol_data()
        dd = db.get_all_symbol_data()
        print(dd.keys())

    if False:
        df = db.get_symbol_data('MG.TO')

    if True:
        df = db.get_all_symbol_single_data_item('Close')
        print(df)
        #df = db.get_all_symbol_single_data_item('Volume')
        #print(df.head())

    if False:
        db = sdm.StockDBMgr('../stock_db/test',
                            datetime.date(2017, 1, 1),
                            datetime.date(2018, 1, 1),
                            False)
        df = db.get_symbol_data(db.get_all_symbols()[0])
        print(df.describe())


if __name__ == '__main__':
    _main()
