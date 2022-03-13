import finance_utils as fu
import datetime
import numpy as np
import pytest


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


def test_symbol_filename():
    d = 'stock_db/test'
    s = 'SPY'
    f = fu.symbol_to_filename(s, d)

    assert len(f) > 0
    assert f.endswith('.csv')
    assert fu.filename_to_symbol(f) == 'SPY'
    assert fu.filename_to_symbol(f.upper()) == 'SPY'


def test_validate_symbol_data_ok():
    assert fu.validate_symbol_data('stock_db/test/SPY.csv')


def test_validate_symbol_data_bad():
    filename = 'stock_db/empty3/bad_csv.txt'
    with open(filename, 'w') as f:
        f.write('thisisabadcsvheader\n')
        f.write('1,2,3\n')
        f.write('4,5,6\n')
    assert not fu.validate_symbol_data(filename)



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


def test_load_data_frame():
    f = 'stock_db/test/SPY.csv'
    df = fu.load_data_frame(f, datetime.date(2018, 1, 1), datetime.date(2018, 4, 1), True)

    col = list(df.columns)
    test_col = ['Open', 'High', 'Low', 'Close', 'Volume']
    assert len(col) == len(test_col)

    for c in test_col:
        assert c in col


def test_load_data_frame_no_adj():
    f = 'stock_db/test/SPY.csv'
    df = fu.load_data_frame(f, datetime.date(2018, 1, 1), datetime.date(2018, 4, 1), False)

    col = list(df.columns)
    test_col = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    assert len(col) == len(test_col)

    for c in test_col:
        assert c in col


def test_normalize_data_frame():
    f = 'stock_db/test/SPY.csv'
    df = fu.load_data_frame(f, datetime.date(2018, 1, 1), datetime.date(2018, 4, 1))
    # Not applicable for a single stock, but just to test...
    assert fu.normalize_data_frame(df).iloc[0].mean() == 1.0


def test_fill_nan_data_notinplace():
    f = 'stock_db/test/SPY.csv'
    df = fu.load_data_frame(f, datetime.date(2018, 1, 1), datetime.date(2018, 4, 1))
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
    f = 'stock_db/test/SPY.csv'
    df = fu.load_data_frame(f, datetime.date(2018, 1, 1), datetime.date(2018, 4, 1))
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
