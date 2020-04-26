import finance_utils as fu
import datetime
import numpy as np


def test_1():
    sf = 'stock_db/dj.txt'
    assert len(fu.get_symbols_from_file(sf)) > 0


def test_2():
    d = 'stock_db/test'
    s = 'SPY'
    f = fu.symbol_to_filename(s, d)

    assert len(f) > 0
    assert f.endswith('.csv')
    assert fu.filename_to_symbol(f) == 'SPY'
    assert fu.filename_to_symbol(f.upper()) == 'SPY'


def test_3_1():
    assert fu.validate_symbol_data('stock_db/test/SPY.csv')


def test_3_2():
    filename = 'stock_db/empty3/bad_csv.txt'
    with open(filename, 'w') as f:
        f.write('thisisabadcsvheader\n')
        f.write('1,2,3\n')
        f.write('4,5,6\n')
    assert not fu.validate_symbol_data(filename)


def test_4():
    d = 'stock_db/test'
    assert len(fu.get_all_symbols(d)) > 3


def test_5():
    s = 'SPY'
    d = 'stock_db/empty2'
    start_date = datetime.date(2010, 1, 1)
    end_date = datetime.date(2012, 1, 1)
    fu.download_data(s, d, start_date, end_date)
    assert len(fu.get_all_symbols(d)) == 1


def test_6():
    d = 'stock_db/empty2'
    start_date = datetime.date(2000, 1, 1)
    end_date = datetime.date.today()
    fu.update_all_symbols(d, start_date, end_date)
    assert len(fu.get_all_symbols(d)) == 1


def test_7():
    assert len(fu.get_symbols_from_file('stock_db/test.txt')) > 3


def test_8():
    f = 'stock_db/test/SPY.csv'
    df = fu.load_data_frame(f, datetime.date(2018, 1, 1), datetime.date(2018, 4, 1))

    assert len(fu.get_date(df)) > 0
    assert len(fu.get_open(df)) > 0
    assert len(fu.get_high(df)) > 0
    assert len(fu.get_low(df)) > 0
    assert len(fu.get_close(df)) > 0
    assert len(fu.get_volume(df)) > 0


def test_9():
    f = 'stock_db/test/SPY.csv'
    df = fu.load_data_frame(f, datetime.date(2018, 1, 1), datetime.date(2018, 4, 1))
    # Not applicable for a single stock, but just to test...
    assert fu.normalize_data_frame(df).iloc[0].mean() == 1.0


def test_10():
    f = 'stock_db/test/SPY.csv'
    df = fu.load_data_frame(f, datetime.date(2018, 1, 1), datetime.date(2018, 4, 1))
    # Test by adding some NaN
    df.iloc[0:10, 0] = np.nan  # beginning
    df.iloc[11:20, 1] = np.nan  # middle
    df.iloc[-10:, 2] = np.nan  # end
    assert df.isna().any().any()
    fu.fill_nan_data(df)
    assert not df.isna().any().any()


def test_good_url():
    url_array = [
        'https://www.google.ca',
        'https://www.tmall.com',
        'https://tmxmoney.com/en/index.html',
    ]
    for u in url_array:
        assert len(fu.download_url(u)) > 100


def test_bad_url():
    url_array = [
        'https://cloud.iexapis.com',
        'https://cloud.iexapis.com/stable/stock/aapl/batch',
        'https://cloud.iexapis.com/stable/stock/aapl/batch?types=quote,news,chart&range=1m&last=10',
        'https://www.bad234123421342134.com',
    ]
    for u in url_array:
        assert len(fu.download_url(u)) == 0
