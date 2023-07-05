# -------------------------------------------------------------------------------
# Various test with the pandas library
# http://pandas.pydata.org/pandas-docs/stable/dsintro.html
# -------------------------------------------------------------------------------

# To make print working for Python2/3
from __future__ import print_function

import string
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_test():
    df1 = pd.read_csv('../portfolio.csv', index_col='Date', parse_dates=True)
    df2 = pd.read_csv('../portfolio2.csv', index_col='Date', parse_dates=True)

    df = df2.join(df1, how='outer')
    df.interpolate(method='linear', inplace=True)
    df.plot()
    plt.show()


def dataframe_test2():
    nrow = 8
    ncol = 5
    dates = pd.date_range('2000-01-01', periods=nrow)
    df = pd.DataFrame(
        data=np.random.randn(nrow, ncol),
        index=dates,
        columns=list(string.ascii_uppercase[0:ncol]))
    df.rename_axis('Date', axis='rows', inplace=True)
    df.rename_axis('DATA', axis='columns', inplace=True)
    print(df)
    df['A'].plot(label='Label A', linestyle='None', marker='x')
    df['B'].plot(label='Label B', linestyle='None', marker='o')
    plt.legend()
    plt.show()

    df.plot()
    plt.show()


def dataframe_test():
    # This stock has a split
    f = '../stock_db/tsx/NA.TO.csv'
    df = pd.read_csv(f, index_col='Date', parse_dates=True, na_values='nan')
    print(df.describe())
    print(df.head())

    df.sort_index(inplace=True)

    # Column indexing
    print(df['Close'][:10])  # (and row indexing)
    print(df['Close'].max())
    print(df['Close'].mean())
    print(df['Close'].std())
    print(df[['Open', 'Close']].mean())  # multi column

    # Row indexing
    print(df.iloc[0])  # Integer based
    print(df.iloc[0:3])  # Integer based, multi row
    print(df.loc['2017-02-06'])  # Label based
    print(df.loc['2017-02-06':'2017-02-10'])  # Label based, multi row

    # Both
    print(df.loc['2018-01-04', 'High'])
    # From date & up, Open & Close only
    print(df.loc['2020-01-01':, ['Open', 'Close']])
    # Date range, Open & Close only
    print(df.loc['2020-01-01':'2020-01-31', ['Open', 'Close']])

    # NA test
    print(df.isna().any(1).sum())
    print(df.isna().all(1).sum())

    # Adjusting Columns based on Adjusted Close
    r = df['Adj Close'] / df['Close']  # ratio
    for col in ['Open', 'High', 'Low', 'Close']:
        df[col] *= r

    df.drop('Adj Close', axis=1, inplace=True)

    print(df.head())
    print(df.describe())


def _main():
    plot_test()
    dataframe_test2()
    dataframe_test()


if __name__ == '__main__':
    _main()
