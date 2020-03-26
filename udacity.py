# For online course: https://classroom.udacity.com/courses/ud501

import datetime
import matplotlib.pyplot as plt
import stock_db_mgr as sdm

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
    pass


def _main():
    # Reverser order as seen in course
    test_normalize()
    test_slice()
    test_multi_symbol()
    test_plot()
    test_pandas()


if __name__ == '__main__':
    _main()
