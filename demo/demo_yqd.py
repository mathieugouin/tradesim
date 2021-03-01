# To make print working for Python2/3
from __future__ import print_function

# User
import yqd


def _main():
    print("main")

    tickers = ['IBM', 'ZCN.TO']
    for ticker in tickers:
        print('===', ticker, '===')
        lines = yqd.load_yahoo_quote(ticker, '20180212', '20180213').split('\n')
        for l in lines:
            print(l)


if __name__ == "__main__":
    _main()
