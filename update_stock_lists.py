# To make print working for Python2/3
from __future__ import print_function

import pandas as pd


def update_dj():
    """Update Dow Jones list"""
    h = pd.read_html('https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average', keep_default_na=False)
    df = h[1]  # 2nd table

    # Make sure Symbol column is first, only keep relevant columns
    df = df.loc[:, ['Symbol', 'Company']]

    df.sort_values(by='Symbol', inplace=True)

    # yahoo use - instead of .
    df['Symbol'] = df['Symbol'].map(lambda s: s.replace('.', '-'))

    # insert comment
    df.rename(columns={'Symbol': '# Symbol'}, inplace=True)

    # write
    df.to_csv('stock_db/dj.txt', sep='\t', index=False, encoding='utf-8')


def update_tsx():
    """Update TSX list"""
    h = pd.read_html('https://en.wikipedia.org/wiki/S%26P/TSX_Composite_Index', keep_default_na=False)

    df = None
    found = False
    for df in h:
        if 'Ticker' in df.columns and 'Company' in df.columns:
            found = True
            break

    if not found:
        return

    df.rename(columns={'Ticker': 'Symbol'}, inplace=True)

    # Make sure Symbol column is first, only keep relevant columns
    df = df.loc[:, ['Symbol', 'Company']]

    df.sort_values(by='Symbol', inplace=True)

    # yahoo use - instead of .
    df['Symbol'] = df['Symbol'].map(lambda s: s.replace('.', '-'))

    # .TO for yahoo
    df['Symbol'] = df['Symbol'].map(lambda s: s + '.TO')

    # insert comment
    df.rename(columns={'Symbol': '# Symbol'}, inplace=True)

    # write
    df.to_csv('stock_db/tsx.txt', sep='\t', index=False, encoding='utf-8')


def update_sp500():
    """Update SP-500 list"""
    h = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies', keep_default_na=False)
    df = h[0]  # first table

    # Make sure Symbol column is first, only keep relevant columns
    df = df.loc[:, ['Symbol', 'Security']]

    df.rename(columns={'Security': 'Company'}, inplace=True)

    df.sort_values(by='Symbol', inplace=True)

    # yahoo use - instead of .
    df['Symbol'] = df['Symbol'].map(lambda s: s.replace('.', '-'))

    # insert comment
    df.rename(columns={'Symbol': '# Symbol'}, inplace=True)

    # write
    df.to_csv('stock_db/sp500.txt', sep='\t', index=False, encoding='utf-8')


def _main():
    update_dj()
    update_tsx()  # TBD wiki not fully up-to-date
    update_sp500()


if __name__ == '__main__':
    _main()
