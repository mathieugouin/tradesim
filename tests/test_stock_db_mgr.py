import datetime
import os
import pytest
import finance_utils as fu
import stock_db_mgr as sdm

_STOCK_DB_TEST_PATH = './stock_db/test'
_STOCK_DB_TEST_SYMBOLS = fu.get_symbols_from_file("./stock_db/test.txt")


@pytest.mark.parametrize("symbol", _STOCK_DB_TEST_SYMBOLS)
def test_creation_default_date_range(symbol):
    db = sdm.StockDBMgr(_STOCK_DB_TEST_PATH)
    df = db.get_symbol_data(symbol)
    start = datetime.date(2020, 3, 16)
    stop = datetime.date(2020, 3, 20)
    assert df.iloc[0].name.date() < start
    assert df.iloc[-1].name.date() > stop


@pytest.mark.parametrize("symbol", _STOCK_DB_TEST_SYMBOLS)
def test_creation_custom_date_range(symbol):
    start = datetime.date(2020, 3, 16)
    stop = datetime.date(2020, 3, 20)
    db = sdm.StockDBMgr(_STOCK_DB_TEST_PATH, start, stop)
    df = db.get_symbol_data(symbol)
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
    db = sdm.StockDBMgr(_STOCK_DB_TEST_PATH)
    symbol_list_db = db.get_all_symbols()
    symbol_list_fu = fu.get_symbols_from_file("./stock_db/test.txt")
    assert len(symbol_list_db) == len(symbol_list_fu)
    for symbol in symbol_list_db:
        assert symbol in symbol_list_fu


@pytest.mark.webtest
def test_download_data(tmp_path):
    symbol = 'SPY'
    db_dir = tmp_path
    db = sdm.StockDBMgr(db_dir)
    assert symbol not in db._dic
    db.get_symbol_data(symbol)
    assert symbol in db._dic
    db.download_data(symbol)
    assert symbol not in db._dic


@pytest.mark.toimprove
@pytest.mark.parametrize("symbol", _STOCK_DB_TEST_SYMBOLS)
def test_validate_symbol_data(symbol):
    end = datetime.date.today()
    start = end - datetime.timedelta(days=365)
    db = sdm.StockDBMgr(_STOCK_DB_TEST_PATH, start, end)
    assert db.validate_symbol_data(symbol)


def test_validate_symbol_data_fail(tmp_path):
    symbol = 'SPY'
    db_dir = tmp_path
    # create a corrupted CSV file
    file = fu.symbol_to_filename(symbol, db_dir)
    with open(file, 'w') as file_handle:
        file_handle.write('this_is_a_bad_csv_header\n')
        file_handle.write('1,2,3\n')
        file_handle.write('4,5,6\n')

    # Confirm invalid
    db = sdm.StockDBMgr(db_dir)
    assert not db.validate_symbol_data(symbol)


@pytest.mark.webtest
def test_update_all_symbols(tmp_path):
    symbol = 'SPY'
    db_dir = tmp_path
    filename = fu.symbol_to_filename(symbol, db_dir)
    assert not os.path.exists(filename)
    db = sdm.StockDBMgr(db_dir)
    assert symbol not in db._dic
    # Get a single symbol
    df = db.get_symbol_data(symbol)
    assert len(df) > 100
    assert os.path.exists(filename)
    # Symbol is in cache
    assert symbol in db._dic
    db.update_all_symbols()
    # Symbol is not in cache
    assert symbol not in db._dic


def test_get_symbol_data():
    db = sdm.StockDBMgr(_STOCK_DB_TEST_PATH)
    symbol = "SPY"
    df1 = db.get_symbol_data(symbol)
    assert df1.axes[1].name == symbol
    df2 = db.get_symbol_data(symbol)
    assert (df1 == df2).all().all()
    assert len(df1) == len(df2)
    assert df1 is df2


@pytest.mark.webtest
@pytest.mark.parametrize("symbol", [
    # Not a ticker:
    'BAAD',

    # Invalid ticker:
    # A stock symbol or ticker is a unique series of letters assigned
    # to a security for trading purposes. Stocks listed on the
    # New York Stock Exchange (NYSE) can have four or fewer letters.
    # Nasdaq-listed securities can have up to five characters.
    'XXXZZZ',
])
def test_get_symbol_data_bad(tmp_path, symbol):
    db_dir = tmp_path
    db = sdm.StockDBMgr(db_dir)
    df = db.get_symbol_data(symbol)
    assert df is None


def test_get_all_symbol_data():
    db = sdm.StockDBMgr(_STOCK_DB_TEST_PATH)
    dic = db.get_all_symbol_data()
    all_symbols = db.get_all_symbols()
    assert len(all_symbols) == len(dic.keys())
    for s in all_symbols:
        assert s in dic
        assert dic[s].axes[1].name == s


def test_get_all_symbol_dataframe():
    db = sdm.StockDBMgr(_STOCK_DB_TEST_PATH)
    df = db.get_all_symbol_dataframe()
    db_symbols = db.get_all_symbols()
    assert df is not None
    assert df.axes[1].nlevels == 2
    assert df.axes[1].names[0] == "Symbol"
    assert df.axes[1].names[1] == "Data"
    dic = {}
    for col in df.axes[1]:
        if col[0] in dic:
            dic[col[0]].append(col[1])
        else:
            dic[col[0]] = [col[1]]

    test_data = ['Open', 'High', 'Low', 'Close', 'Volume']
    assert len(db_symbols) == len(dic)
    for symbol in dic:
        assert symbol in db_symbols
        assert len(test_data) == len(dic[symbol])
        for data in dic[symbol]:
            assert data in test_data


def test_get_all_symbol_single_data_item():
    db = sdm.StockDBMgr(_STOCK_DB_TEST_PATH)
    symbol_list = db.get_all_symbols()
    df1 = db.get_symbol_data(symbol_list[0])
    for data in df1.columns:
        df = db.get_all_symbol_single_data_item(data)
        assert df.axes[1].name == data
        for s in symbol_list:
            assert s in df

    df = db.get_all_symbol_single_data_item('BadData')
    assert df is None
