# For online course: https://classroom.udacity.com/courses/ud501

import datetime
import matplotlib.pyplot as plt
import numpy as np
import stock_db_mgr as sdm
import finance_utils as fu

startdate = datetime.date(2010, 1, 1)
enddate = datetime.date.today()

# Create data base:
db = sdm.CStockDBMgr('./stock_db/test', startdate, enddate)


def test_pandas():
    df = db.getSymbolData('AAPL')
    print df.head()
    print df.describe()
    print df[10:21]


def test_plot():
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

    r1 = np.random.random(size=(2, 3))
    r2 = np.random.normal(size=(2,3))
    print r1
    print r2

    # TBD continue at lesson 4 : 18 (boolean mask)

    pass


def _main():
    # Reverser order as seen in course
    test_np_arrays()
    test_plot()
    test_normalize()
    test_slice()
    test_multi_symbol()
    test_plot()
    test_pandas()


if __name__ == '__main__':
    _main()
