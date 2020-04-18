import datetime
import stock_db_mgr as sdm

def test_get_all_symbols():
    db = sdm.StockDBMgr('./stock_db/test', datetime.date(2017, 1, 1), datetime.date(2018, 1, 1))
    symbol_list = db.get_all_symbols()
    assert len(symbol_list) > 0
