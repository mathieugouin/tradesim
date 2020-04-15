# For online course: https://classroom.udacity.com/courses/ud501

# To make print working for Python2/3
from __future__ import print_function

import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import stock_db_mgr as sdm
import finance_utils as fu

start_date = datetime.date(2010, 1, 1)
# end_date  = datetime.date(2014, 1, 1)
end_date = datetime.date.today()

# Create data base:
db = sdm.StockDBMgr('./stock_db/test', start_date, end_date)


def test_pandas():
    df = db.get_symbol_data('AAPL')
    print(df.head())
    print(df.describe())
    print(df[10:21])


def test_plot_data():
    df = db.get_symbol_data('IBM')
    df['High'].plot()
    plt.show()

    df[['Low', 'High']].plot()
    plt.show()


def test_multi_symbol():
    df = db.get_all_symbol_single_data_item('Close')
    print(df[['AAPL', 'IBM']].max())

    df = db.get_all_symbol_single_data_item('Volume')
    print(df[['AAPL', 'IBM']].mean())


def test_slice():
    df = db.get_all_symbol_single_data_item('Close')

    df_row = df.loc['2010-01-01':'2010-01-10']
    print(df_row)

    df_col = df[['GOOG', 'IBM']]
    print(df_col.head(1))  # too big

    df_both = df.loc['2010-01-01':'2010-01-10', ['AAPL', 'SPY']]
    print(df_both)


def test_normalize():
    df = db.get_all_symbol_single_data_item('Close').loc[:, ['AAPL', 'GLD', 'IBM', 'SPY']]
    df2 = fu.normalize_data_frame(df)
    plot_data(df2)


def get_data(symbols, dates):
    df = db.get_all_symbol_single_data_item('Close')
    df = df.loc[:, symbols]  # keep only required symbols
    df = df.reindex(dates)  # keep only required dates
    df.dropna(inplace=True)  # flush nan
    return df


def plot_data(df, title="Stock Prices", ylabel="Prices"):
    """Plot the data frame"""
    ax = df.plot(title=title)
    ax.set_xlabel("Date")
    ax.set_ylabel(ylabel)
    plt.grid()
    plt.show()


def plot_selected(df, stocks, sd, ed):
    df2 = df.loc[sd:ed, stocks]
    plot_data(df2)
    pass


def test_plot():
    df = db.get_all_symbol_single_data_item('Close')
    df2 = fu.normalize_data_frame(df)
    plot_selected(df2, ['SPY', 'IBM'], '2010-03-01', '2010-04-01')
    pass


def test_np_arrays():
    a1 = np.ones(4)
    a2 = np.zeros((3, 5))
    print(a1)
    print(a2)

    r1 = np.random.rand(2, 3)
    r2 = np.random.randn(2, 3)
    print(r1)
    print(r2)

    a = np.random.randn(5)
    print(a)
    indices = np.array([1,1,2,3])
    print(indices)
    print(a[indices])

    a = np.array([(20,25,10,23,26,32,10,5,0), (0,2,50,20,0,1,28,5,0)])
    print(a)
    m = a.mean()
    print(m)
    print(a[a < m])
    a[a < m] = -1
    print(a)

    a = np.array([(1,2,3,4,5), (10,20,30,40,50)])
    print(a)
    print(2 * a)
    print(a / 2)
    print(a / 2.0)

    pass


def test_time_series():
    dates = pd.date_range('2010-01-01', '2012-12-31')
    symbols = ['SPY', 'XOM', 'GOOG', 'GLD']
    df = get_data(symbols, dates)
    plot_data(df)

    print('Mean: {}'.format(df.mean()))
    print('Median: {}'.format(df.median()))
    print('Std dev: {}'.format(df.std()))


def test_rolling_stats():
    # Ref: https://pandas.pydata.org/pandas-docs/stable/user_guide/computation.html
    c = db.get_symbol_data('SPY').loc[:, 'Close']
    r = c.rolling(window=60)

    d = {
        'raw':  c,
        'mean': r.mean(),
        'min':  r.min(),
        'max':  r.max(),
        'std':  r.std()
    }

    df = pd.DataFrame(d)
    df.plot()
    plt.show()


def get_bollinger_bands(series, window):
    r = series.rolling(window=window)
    rm = r.mean()
    rs = r.std()
    upper_band = rm + 2.0 * rs
    lower_band = rm - 2.0 * rs

    return rm, upper_band, lower_band


def test_rolling_stats2():
    df = get_data(['SPY'], pd.date_range('2019-01-01', '2020-04-01'))
    ax = df['SPY'].plot(title='SPY Bollinger Bands', label='SPY', legend=True)

    rolling_mean, upper_band, lower_band = get_bollinger_bands(df['SPY'], 20)

    rolling_mean.plot(style=':', label='Rolling mean', ax=ax, legend=True)
    upper_band.plot(style='--', label='Upper band', ax=ax, legend=True)
    lower_band.plot(style='--', label='Lower band', ax=ax, legend=True)

    plt.show()


def test_daily_returns():
    # 5.10
    dates = pd.date_range('2012-07-01', '2012-07-31')  # one month only
    symbols = ['SPY', 'XOM']
    df = get_data(symbols, dates)
    plot_data(df)

    # Compute daily returns
    dr = df.pct_change() * 100.0  # make it directly in %
    #dr.iloc[0] = 0.0  # asked by quiz, not sure it makes sense
    plot_data(dr, title='Daily Returns', ylabel='%')
    #dr.plot(marker='.', linestyle='')  # alternate plot style


def test_cumulative_returns():
    # 5.12
    dates = pd.date_range('2012-01-01', '2012-12-31')  # one year
    symbols = ['SPY', 'XOM']
    df = get_data(symbols, dates)
    # plot_data(df)

    # Compute cumulative return
    cr = (df / df.iloc[0] - 1.0) * 100.0  # make it in % directly
    plot_data(cr, title='Cumulative Returns', ylabel='%')
    pass


def fudge_data():
    f = 'stock_db/test/JAVA.csv'
    df = pd.read_csv(f + '.bak', index_col='Date')

    # Fudge data
    df.loc[:, 'Volume'] = df.loc[:, 'Volume'] / 100.0
    df.iloc[:, 1:-1] = df.iloc[:, 1:-1] * 0.7
    df.to_csv(f)


def test_missing_data():
    df_gap = db.get_all_symbol_single_data_item('Close').loc[:, ['SPY', 'JAVA', 'FAKE1', 'FAKE2']]
    df_gap.plot()
    plt.show()

    df = db.get_all_symbol_single_data_item('Close').loc[:, ['SPY', 'JAVA', 'FAKE1', 'FAKE2']]
    fu.fill_nan_data(df)
    df.plot()
    plt.show()


def test_histogram():
    # TBD continue @ 7.1
    pass


def _main():
    # Reverse order as seen in course

    test_histogram()
    test_missing_data()
    test_cumulative_returns()
    test_daily_returns()
    test_rolling_stats2()
    test_rolling_stats()
    test_time_series()
    test_np_arrays()
    test_plot()
    test_normalize()
    test_slice()
    test_multi_symbol()
    test_plot_data()
    test_pandas()


if __name__ == '__main__':
    _main()
