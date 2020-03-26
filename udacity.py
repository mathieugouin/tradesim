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


def test_multi_symbol():
    df = db.getAllSymbolDataSingleItem('Close')
    print df[['AAPL', 'IBM']].max()

    df = db.getAllSymbolDataSingleItem('Volume')
    print df[['AAPL', 'IBM']].mean()
    pass


def test_plot():
    df = db.getSymbolData('IBM')
    df['High'].plot()
    plt.show()

    df[['Low', 'High']].plot()
    plt.show()

    pass


def _main():
    # Reverser order as seen in course
    test_multi_symbol()
    test_plot()
    test_pandas()


if __name__ == '__main__':
    _main()
