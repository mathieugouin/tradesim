# For online course: https://classroom.udacity.com/courses/ud501

import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import stock_db_mgr as sdm
import finance_utils as fu

start_date = datetime.date(2010, 1, 1)
#end_date  = datetime.date(2014, 1, 1)
end_date = datetime.date.today()

# Create data base:
db = sdm.CStockDBMgr('./stock_db/test', start_date, end_date)


def test_pandas():
    df = db.getSymbolData('AAPL')
    print df.head()
    print df.describe()
    print df[10:21]


def test_plot_data():
    df = db.getSymbolData('IBM')
    df['High'].plot()
    plt.show()

    df[['Low', 'High']].plot()
    plt.show()
    pass


def test_multi_symbol():
    df = db.getAllSymbolDataSingleItem('Close')
    print df[['AAPL', 'IBM']].max()

    df = db.getAllSymbolDataSingleItem('Volume')
    print df[['AAPL', 'IBM']].mean()
    pass


def test_slice():
    df = db.getAllSymbolDataSingleItem('Close')

    df_row = df.loc['2010-01-01':'2010-01-10']
    print df_row

    df_col = df[['GOOG', 'IBM']]
    print df_col.head(1)  # too big

    df_both = df.loc['2010-01-01':'2010-01-10', ['AAPL', 'SPY']]
    print df_both
    pass


def test_normalize():
    df = db.getAllSymbolDataSingleItem('Close')
    df2 = fu.normalizeDataFrame(df)
    plot_data(df2)
    pass


def get_data(symbols, dates):
    df = db.getAllSymbolDataSingleItem('Close')
    df = df.loc[dates, symbols]
    df.dropna(inplace=True)
    return df


def plot_data(df, title="Stock Prices"):
    """Plot the data frame"""
    ax = df.plot(title=title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Prices")
    plt.grid()
    plt.show()


def plot_selected(df, stocks, sd, ed):
    df2 = df.loc[sd:ed, stocks]
    plot_data(df2)
    pass


def test_plot():
    df = db.getAllSymbolDataSingleItem('Close')
    df2 = fu.normalizeDataFrame(df)
    plot_selected(df2, ['SPY', 'IBM'], '2010-03-01', '2010-04-01')
    pass


def test_np_arrays():
    a1 = np.ones(4)
    a2 = np.zeros((3, 5))
    print a1
    print a2

    r1 = np.random.rand(2, 3)
    r2 = np.random.randn(2, 3)
    print r1
    print r2

    a = np.random.randn(5)
    print a
    indices = np.array([1,1,2,3])
    print indices
    print a[indices]

    a = np.array([(20,25,10,23,26,32,10,5,0), (0,2,50,20,0,1,28,5,0)])
    print a
    m = a.mean()
    print m
    print a[a < m]
    a[a < m] = -1
    print a

    a = np.array([(1,2,3,4,5), (10,20,30,40,50)])
    print a
    print 2 * a
    print a / 2
    print a / 2.0

    pass


def test_time_series():
    dates = pd.date_range('2010-01-01', '2012-12-31')
    symbols = ['SPY', 'XOM', 'GOOG', 'GLD']
    df = get_data(symbols, dates)
    plot_data(df)

    print 'Mean:', df.mean()
    print 'Median', df.median()
    print 'Std dev', df.std()


def test_rolling_stats():
    s = pd.Series(np.random.randn(1000), index=pd.date_range('2000-01-01', periods=1000))
    c = s.cumsum()

    r = c.rolling(window=60)

    d = {}
    d['raw'] = c
    d['mean'] = r.mean()
    d['min'] = r.min()
    d['max'] = r.max()

    df = pd.DataFrame(d)
    df.plot()
    plt.show()

    # Lesson 5.7

    pass


def _main():
    # Reverse order as seen in course
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
