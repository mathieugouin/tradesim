import datetime
import pytest
import stock_db_mgr as sdm


_STOCK_DB_TEST_PATH = './stock_db/test'


def test_creation_default_date_range():
    db = sdm.StockDBMgr(_STOCK_DB_TEST_PATH)
    df = db.get_symbol_data('SPY')
    start = datetime.date(2020, 3, 16)
    stop = datetime.date(2020, 3, 20)
    assert df.iloc[0].name.date() < start
    assert df.iloc[-1].name.date() > stop


def test_creation_custom_date_range():
    start = datetime.date(2020, 3, 16)
    stop = datetime.date(2020, 3, 20)
    db = sdm.StockDBMgr(_STOCK_DB_TEST_PATH, start, stop)
    df = db.get_symbol_data('SPY')
    assert df.iloc[0].name.date() == start
    assert df.iloc[-1].name.date() == stop


def test_print():
    db = sdm.StockDBMgr(_STOCK_DB_TEST_PATH)
    str1 = str(db)
    assert len(str1) > 0
    print(str1)
    # Cache some symbols
    _ = db.get_all_symbol_data()
    str2 = str(db)
    assert len(str2) > len(str1)
    print(str2)


def test_get_all_symbols():
    db = sdm.StockDBMgr(_STOCK_DB_TEST_PATH, datetime.date(2017, 1, 1), datetime.date(2018, 1, 1))
    symbol_list = db.get_all_symbols()
    assert len(symbol_list) > 3


@pytest.mark.webtest
def test_download_data():
    db = sdm.StockDBMgr(_STOCK_DB_TEST_PATH)
    assert 'SPY' not in db._dic
    db.get_symbol_data('SPY')
    assert 'SPY' in db._dic
    db.download_data('SPY')
    assert 'SPY' not in db._dic


def test_validate():
    db = sdm.StockDBMgr(_STOCK_DB_TEST_PATH)
    for s in db.get_all_symbols():
        assert db.validate_symbol_data(s)


@pytest.mark.webtest
def test_update_all_symbols():
    db = sdm.StockDBMgr('./stock_db/empty')
    assert 'SPY' not in db._dic
    # Get a single symbol
    db.get_symbol_data('SPY')
    assert 'SPY' in db._dic
    db.update_all_symbols()
    assert 'SPY' not in db._dic


def test_get_symbol_data():
    db = sdm.StockDBMgr(_STOCK_DB_TEST_PATH)
    df1 = db.get_symbol_data('SPY')
    df2 = db.get_symbol_data('SPY')
    assert (df1 == df2).all().all()
    assert len(df1) == len(df2)
    assert df1 is df2
    assert 'Adj Close' not in df1.columns


def test_get_symbol_data_noadj():
    db = sdm.StockDBMgr(_STOCK_DB_TEST_PATH, adjust_price=False)
    df1 = db.get_symbol_data('SPY')
    df2 = db.get_symbol_data('SPY')
    assert (df1 == df2).all().all()
    assert len(df1) == len(df2)
    assert df1 is df2
    assert 'Adj Close' in df1.columns


@pytest.mark.webtest
def test_get_symbol_data_bad_1():
    db = sdm.StockDBMgr('./stock_db/bad')
    df = db.get_symbol_data('BAAD')
    assert df is None


@pytest.mark.webtest
def test_get_symbol_data_bad_2():
    db = sdm.StockDBMgr('./stock_db/bad')
    # A stock symbol or ticker is a unique series of letters assigned
    # to a security for trading purposes. Stocks listed on the
    # New York Stock Exchange (NYSE) can have four or fewer letters.
    # Nasdaq-listed securities can have up to five characters.
    df = db.get_symbol_data('XXXZZZ')  # Invalid ticker
    assert df is None


def test_get_all_symbol_data():
    db = sdm.StockDBMgr(_STOCK_DB_TEST_PATH)
    dic = db.get_all_symbol_data()
    for s in db.get_all_symbols():
        assert s in dic


@pytest.mark.toimprove
def test_get_all_symbol_dataframe():
    db = sdm.StockDBMgr(_STOCK_DB_TEST_PATH)
    df = db.get_all_symbol_dataframe()
    assert df is not None


@pytest.mark.toimprove
def test_get_all_symbol_single_data_item():
    db = sdm.StockDBMgr(_STOCK_DB_TEST_PATH, adjust_price=False)
    symbol_list = db.get_all_symbols()
    df1 = db.get_symbol_data(symbol_list[0])
    for data in df1.columns:
        df = db.get_all_symbol_single_data_item(data)
        # TBD check that df name matches the data
        for s in symbol_list:
            assert s in df

    df = db.get_all_symbol_single_data_item('BadData')
    assert df is None
