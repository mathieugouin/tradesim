import datetime
import stock_db_mgr as sdm


def test_creation_default_date_range():
    db = sdm.StockDBMgr('./stock_db/test')
    df = db.get_symbol_data('SPY')
    start = datetime.date(2020, 3, 16)
    stop = datetime.date(2020, 3, 20)
    assert df.iloc[0].name.date() < start
    assert df.iloc[-1].name.date() > stop


def test_creation_custom_date_range():
    start = datetime.date(2020, 3, 16)
    stop = datetime.date(2020, 3, 20)
    db = sdm.StockDBMgr('./stock_db/test', start, stop)
    df = db.get_symbol_data('SPY')
    assert df.iloc[0].name.date() == start
    assert df.iloc[-1].name.date() == stop


def test_get_all_symbols():
    db = sdm.StockDBMgr('./stock_db/test', datetime.date(2017, 1, 1), datetime.date(2018, 1, 1))
    symbol_list = db.get_all_symbols()
    assert len(symbol_list) > 3


def test_download_data():
    db = sdm.StockDBMgr('./stock_db/test')
    assert 'SPY' not in db._dic
    db.get_symbol_data('SPY')
    assert 'SPY' in db._dic
    db.download_data('SPY')
    assert 'SPY' not in db._dic


def test_validate():
    db = sdm.StockDBMgr('./stock_db/test')
    for s in db.get_all_symbols():
        assert db.validate_symbol_data(s)


def test_update_all_symbols():
    db = sdm.StockDBMgr('./stock_db/empty')
    assert 'SPY' not in db._dic
    # Get a single symbol
    db.get_symbol_data('SPY')
    assert 'SPY' in db._dic
    db.update_all_symbols()
    assert 'SPY' not in db._dic


def test_get_symbol_data():
    db = sdm.StockDBMgr('./stock_db/test')
    df1 = db.get_symbol_data('SPY')
    df2 = db.get_symbol_data('SPY')
    assert df1 == df2


def test_get_all_symbol_data():
    db = sdm.StockDBMgr('./stock_db/test')
    dic = db.get_all_symbol_data()
    for s in db.get_all_symbols():
        assert s in dic


def test_get_all_symbol_single_data_item():
    db = sdm.StockDBMgr('./stock_db/test')
    df = db.get_all_symbol_single_data_item('Close')
    for s in db.get_all_symbols():
        assert s in df

    df = db.get_all_symbol_single_data_item('BadData')
    assert df is None
