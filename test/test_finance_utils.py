import datetime
import os
import numpy as np
import pandas as pd
import pytest
import finance_utils as fu


_TEST_STOCK_FILE = 'stock_db/test/SPY.csv'


@pytest.mark.parametrize('nb,commission', [
    (0, 0),
    (1, .0035 + 4.95),
    (100, 100 * .0035 + 4.95),
    (495, 495 * .0035 + 4.95),
    (500, (.01 + 0.0035) * 500),
    (995, (.01 + 0.0035) * 995),
    (10000, (0.0035) * 10000 + 9.95),
    (-1, 4.95 + 0.0035),
    (-100, 4.95 + 0.35),
    (-700, (.01 + 0.0035) * 700),
    (-995, (.01 + 0.0035) * 995),
    (-10000, 9.95 + 0.0035 * 10000),
])
def test_calc_commission(nb, commission):
    assert fu.calc_commission(nb) == commission


@pytest.mark.parametrize('nb,commission', [
    (0, 0),
    (1, .0035),
    (495, .0035 * 495),
    (1000, 3.5),
    (-1, 4.95 + 0.0035),
    (-100, 4.95 + 0.35),
    (-700, (.01 + 0.0035) * 700),
    (-995, (.01 + 0.0035) * 995),
    (-10000, 9.95 + 0.0035 * 10000),
])
def test_calc_commission_etf(nb, commission):
    assert fu.calc_commission_etf(nb) == commission


@pytest.mark.parametrize('f', [
        'stock_db/dj.txt',
        'stock_db/indices.txt',
        'stock_db/qt.txt',
        'stock_db/sp500.txt',
        'stock_db/test.txt',
        'stock_db/tsx.txt',
        ])
def test_get_symbols_from_file(f):
    assert len(fu.get_symbols_from_file(f)) > 0


@pytest.mark.parametrize('symbol, directory, filename', [
    ('IBM',         'dir',      'dir/IBM.csv'       ),
    ('NA.TO',       'a/b/c',    'a/b/c/NA.TO.csv'   ),
    ('AP-UN.TO',    '',         'AP-UN.TO.csv'      ),
    ('BRK-A',       '',         'BRK-A.csv'         ),
    ('^GSPC',       '',         '_GSPC.csv'         ),
])
def test_symbol_to_filename(symbol, directory, filename):
    filename_test = fu.symbol_to_filename(symbol, directory)
    assert filename_test == filename
    # Loop back check
    symbol_test = fu.filename_to_symbol(filename_test)
    assert symbol_test == symbol


@pytest.mark.parametrize('filename, symbol', [
    ('dir/IBM.csv',         'IBM'       ),
    ('a/b/c/NA.TO.csv',     'NA.TO'     ),
    ('AP-UN.TO.csv',        'AP-UN.TO'  ),
    ('a/b/BRK-A.csv',       'BRK-A'     ),
    ('_GSPC.csv',           '^GSPC'     ),
])
def test_filename_to_symbol(filename, symbol):
    symbol_test = fu.filename_to_symbol(filename)
    assert symbol_test == symbol


def test_validate_symbol_data_ok():
    assert fu.validate_symbol_data(_TEST_STOCK_FILE)


def test_validate_symbol_data_bad():
    filename = 'stock_db/bad/bad_csv.txt'
    with open(filename, 'w') as f:
        f.write('thisisabadcsvheader\n')
        f.write('1,2,3\n')
        f.write('4,5,6\n')
    assert os.path.exists(filename)
    assert not fu.validate_symbol_data(filename)
    os.remove(filename)
    assert not os.path.exists(filename)


def test_get_all_symbols():
    d = 'stock_db/test'
    assert len(fu.get_all_symbols(d)) > 3


@pytest.mark.webtest
def test_download_data():
    s = 'SPY'
    d = 'stock_db/empty2'
    start_date = datetime.date(2010, 1, 1)
    end_date = datetime.date(2012, 1, 1)
    fu.download_data(s, d, start_date, end_date)
    assert len(fu.get_all_symbols(d)) == 1


@pytest.mark.webtest
def test_update_all_symbols():
    d = 'stock_db/empty2'
    start_date = datetime.date(2000, 1, 1)
    end_date = datetime.date.today()
    fu.update_all_symbols(d, start_date, end_date)
    assert len(fu.get_all_symbols(d)) == 1


def test_load_dataframe_adj():
    f = _TEST_STOCK_FILE
    df = fu.load_dataframe(f, datetime.date(2018, 1, 1), datetime.date(2018, 4, 1), True)
    # DataFrame axes is a list.  It has the row axis labels and column axis labels
    # as the only members. They are returned in that order.
    assert df.axes[1].name == fu.filename_to_symbol(_TEST_STOCK_FILE)

    assert df.notna().all().all()

    df_col = list(df.columns)
    test_col = ['Open', 'High', 'Low', 'Close', 'Volume']
    assert len(df_col) == len(test_col)

    for col in test_col:
        assert col in df_col


def test_load_dataframe_no_adj():
    f = _TEST_STOCK_FILE
    df = fu.load_dataframe(f, datetime.date(2018, 1, 1), datetime.date(2018, 4, 1), False)
    # DataFrame axes is a list.  It has the row axis labels and column axis labels
    # as the only members. They are returned in that order.
    assert df.axes[1].name == fu.filename_to_symbol(_TEST_STOCK_FILE)

    assert df.notna().all().all()

    df_col = list(df.columns)
    test_col = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    assert len(df_col) == len(test_col)

    for col in test_col:
        assert col in df_col


def test_load_dataframe_date_check_1():
    f = _TEST_STOCK_FILE
    start_date = datetime.date(2018, 1, 3)
    stop_date = datetime.date(2018, 1, 17)
    df = fu.load_dataframe(f, start_date, stop_date)
    assert df.iloc[0].name.date() == start_date
    assert df.iloc[-1].name.date() == stop_date


def test_load_dataframe_date_check_2():
    f = _TEST_STOCK_FILE
    start_date = datetime.date(1900, 1, 3)
    stop_date = datetime.date(2100, 1, 17)
    df = fu.load_dataframe(f, start_date, stop_date)
    assert df.iloc[0].name.date() > start_date
    assert df.iloc[-1].name.date() < stop_date


def create_random_df():
    index = pd.date_range(start='2000-01-01', end='2002-01-01')
    columns = list("ABCDE")
    return pd.DataFrame(
        index=index,
        columns=columns,
        data=np.random.random((len(index), len(columns))))


def test_clean_dataframe_no_nan():
    df = create_random_df()
    df2 = fu.clean_dataframe(df, '2000-01-01')
    assert (df == df2).all().all()


def test_clean_dataframe_few_early_nan():
    df = create_random_df()
    df.loc['2000-01-01':'2000-01-03', 'A'] = np.nan
    df2 = fu.clean_dataframe(df, '2000-01-01')
    # Column A should NOT be dropped
    # equals for nan handling
    assert df.equals(df2)


def test_clean_dataframe_many_early_nan():
    df = create_random_df()
    df.loc['2000-01-01':'2000-01-06', 'A'] = np.nan
    df2 = fu.clean_dataframe(df, '2000-01-01')
    # Column A should be dropped
    assert (df.loc[:, 'B':] == df2).all().all()


def test_clean_dataframe_few_late_nan():
    df = create_random_df()
    df.loc['2001-12-30':, 'A'] = np.nan
    df2 = fu.clean_dataframe(df, '2000-01-01')
    # Column A should NOT be dropped
    # equals for nan handling
    assert df.equals(df2)


def test_clean_dataframe_many_late_nan():
    df = create_random_df()
    df.loc['2001-12-28':, 'A'] = np.nan
    df2 = fu.clean_dataframe(df, '2000-01-01')
    # Column A should be dropped
    assert (df.loc[:, 'B':] == df2).all().all()


def test_clean_dataframe_middle_nan():
    df = create_random_df()
    df.loc['2001-01-01':'2001-08-01', ['A', 'C', 'E']] = np.nan
    df2 = fu.clean_dataframe(df, '2000-01-01')
    assert df.equals(df2)


def test_fill_nan_data_notinplace():
    f = _TEST_STOCK_FILE
    df = fu.load_dataframe(f, datetime.date(2018, 1, 1), datetime.date(2018, 4, 1))
    # Test by adding some NaN
    df.iloc[0:10, 0] = np.nan  # beginning
    df.iloc[11:20, 1] = np.nan  # middle
    df.iloc[-10:, 2] = np.nan  # end
    assert df.isna().any().any()
    df2 = fu.fill_nan_data(df)  # default = not inplace
    # New df2 modified:
    assert not df2.isna().any().any()
    # Original df not modified:
    assert df.isna().any().any()


def test_fill_nan_data_inplace():
    f = _TEST_STOCK_FILE
    df = fu.load_dataframe(f, datetime.date(2018, 1, 1), datetime.date(2018, 4, 1))
    # Test by adding some NaN
    df.iloc[0:10, 0] = np.nan  # beginning
    df.iloc[11:20, 1] = np.nan  # middle
    df.iloc[-10:, 2] = np.nan  # end
    assert df.isna().any().any()
    df2 = fu.fill_nan_data(df, inplace=True)
    # Original df modified:
    assert not df.isna().any().any()
    # Returned df2 None
    assert df2 is None


def test_normalize_dataframe():
    f = _TEST_STOCK_FILE
    df = fu.load_dataframe(f, datetime.date(2018, 1, 1), datetime.date(2018, 4, 1))
    # Not applicable for a single stock, but just to test...
    assert fu.normalize_dataframe(df).iloc[0].mean() == 1.0


@pytest.mark.webtest
@pytest.mark.parametrize('u', [
        'https://www.google.ca',
        'https://www.tmall.com',
        'https://tmxmoney.com/en/index.html',
        ])
def test_download_url_good(u):
    assert len(fu.download_url(u)) > 100


@pytest.mark.webtest
@pytest.mark.parametrize('u', [
        'https://cloud.iexapis.com',
        'https://cloud.iexapis.com/stable/stock/aapl/batch',
        'https://cloud.iexapis.com/stable/stock/aapl/batch?types=quote,news,chart&range=1m&last=10',
        'https://www.bad234123421342134.com',
    ])
def test_download_url_bad(u):
    assert len(fu.download_url(u)) == 0
