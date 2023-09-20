# To make print working for Python2/3
from __future__ import print_function

import datetime
import glob
import logging

import stock_db_mgr as sdm

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s%(msecs)03d %(name)-12s %(levelname)-8s %(pathname)s:%(lineno)d %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S.',
                    force=True)


startdate = datetime.date(2023, 1, 1)
today = datetime.date.today()

# Pick one:
# enddate = datetime.date(2018, 2, 22)
enddate = today


def list_all_stockdb():
    txt_list = glob.glob('stock_db/*.txt')
    return [i.replace('.txt', '').replace('stock_db/', '') for i in txt_list]


def check_db(path):
    logging.info("Validating {} ...".format(path))
    # Create data base:
    db = sdm.StockDBMgr('./stock_db/' + path, startdate, enddate, False)

    # db.update_all_symbols()

    inv = []

    symbol_list = db.get_all_symbols()

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

    if len(inv) > 0:
        logging.error("Invalid list of %s : %s" % (path, str(inv)))


def _main():
    db = list_all_stockdb()
    for p in db:
        check_db(p)


if __name__ == '__main__':
    _main()
