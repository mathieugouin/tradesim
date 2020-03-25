#-------------------------------------------------------------------------------
# Various test with the pandas library
# http://pandas.pydata.org/pandas-docs/stable/dsintro.html
#-------------------------------------------------------------------------------

import string
import pandas as pd
import numpy as np
import stock_db_mgr as sdm


def panelTest():
    # Panel (simulated with random values)
    wp = pd.Panel(np.random.randn(3, 10, 5), items=['IBM', 'SPY', 'GLD'],
                  major_axis=pd.date_range('2017-01-01', periods=10),
                  minor_axis=['O', 'H', 'L', 'C', 'V'])
    print wp
    # All stocks, all dates, Open only:
    print wp.ix[:,:,'O']
    # IBM only, all dates, High Low only:
    print wp.ix['IBM', :, ['H', 'L']]


def data_frame_test2():
    nrow = 8
    ncol = 5
    dates = pd.date_range('2000-01-01', periods=nrow)
    df = pd.DataFrame(data=np.random.randn(nrow, ncol), index=dates, columns=list(string.ascii_uppercase[0:ncol]))
    df.rename_axis('Date', inplace=True)
    print df


def dataFrameTest():
    # This stock has a split
    f = 'stock_db/tsx/NA.TO.csv'
    df = pd.read_csv(f, index_col='Date', parse_dates=True, na_values='nan')
    #print df.describe()
    print df.head()

    df.sort_index(inplace=True)

    #df['Close'].plot()
    #df[['Open', 'High', 'Low', 'Close']][:50].plot()
    #df[['Close', 'Adj Close']].plot()

    # Column indexing
    print df['Close'][:10]  # (and row indexing)
    print df['Close'].max()
    print df['Close'].mean()
    print df['Close'].std()

    # Row indexing
    print df.iloc[0]  # Integer based
    print df.loc['2017-02-02']  # Label based

    # Both
    print df.loc['2018-01-04', 'High']
    # From date & up, Open & Close only
    print df.loc['2017-2-2':, ['Open', 'Close']]

    # NA test
    print df.isna().any(1).sum()
    print df.isna().all(1).sum()

    # Adjusting Columns based on Adjusted Close
    r = df['Adj Close'] / df['Close'] # ratio
    for col in ['Open', 'High', 'Low', 'Close']:
        df[col] *= r

    df.drop('Adj Close', axis=1, inplace=True)

    print df.head()
    print df.describe()

def main():
    data_frame_test2()
    dataFrameTest()
    #panelTest()

if __name__ == '__main__':
    main()
