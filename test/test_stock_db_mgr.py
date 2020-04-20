import datetime
import stock_db_mgr as sdm


def test_creation_custom_date_range():
    start = datetime.date(2020, 3, 16)
    stop = datetime.date(2020, 3, 20)
    db = sdm.StockDBMgr('./stock_db/test', start, stop)
    df = db.get_symbol_data('SPY')
    assert df.iloc[0].name.date() == start
    assert df.iloc[-1].name.date() == stop


def test_creation_default_date_range():
    db = sdm.StockDBMgr('./stock_db/test')
    df = db.get_symbol_data('SPY')
    start = datetime.date(2020, 3, 16)
    stop = datetime.date(2020, 3, 20)
    assert df.iloc[0].name.date() < start
    assert df.iloc[-1].name.date() > stop


def test_get_all_symbols():
    db = sdm.StockDBMgr('./stock_db/test', datetime.date(2017, 1, 1), datetime.date(2018, 1, 1))
    symbol_list = db.get_all_symbols()
    assert len(symbol_list) > 0

