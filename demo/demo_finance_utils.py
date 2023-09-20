# To make print working for Python2/3
from __future__ import print_function

import datetime
import numpy as np
import matplotlib.pyplot as plt

import parent_import
import finance_utils as fu


def demo_commission():
    s = np.arange(-2500, 2501)
    c = [fu.calc_commission(i) for i in s]
    plt.plot(s, c)
    plt.show()

    c = [fu.calc_commission_etf(i) for i in s]
    plt.plot(s, c)
    plt.show()


def demo_fu():
    sf = 'stock_db/dj.txt'
    print("symbol file {} contains the following stocks: {}".format(sf, fu.get_symbols_from_file(sf)))

    d = 'stock_db/test'

    s = 'IBM'
    f = fu.symbol_to_filename(s, d)
    print("symbol {} with directory {} gives filename {}".format(s, d, f))
    print("filename {} gives symbol {}".format(f, fu.filename_to_symbol(f)))
    print("filename {} gives symbol {}".format(f.upper(), fu.filename_to_symbol(f.upper())))
    print("validate_symbol_data_file {} = {}".format(f, fu.validate_symbol_data_file(f)))

    print("directory {} contains the following stocks: {}".format(d, fu.get_all_symbols(d)))

    start_date = datetime.date(1900, 1, 1)
    end_date = datetime.date.today()

    if False:
        fu.download_data(s, d, start_date, end_date)
        fu.update_all_symbols(d, start_date, end_date)

    df = fu.load_dataframe(f, datetime.date(2018, 1, 1), datetime.date(2018, 4, 1))
    print(df.describe())
    print(df.head())

    # Not applicable for a single stock, but just to test...
    print(fu.normalize_dataframe(df).head())

    # Test by adding some NaN
    df.iloc[0:10, 0] = np.nan  # beginning
    df.iloc[11:20, 1] = np.nan  # middle
    df.iloc[-10:, 2] = np.nan  # end
    print(df.isna().any())
    fu.fill_nan_data(df, inplace=True)
    print(df.isna().any())

    url_array = [
        'https://www.google.ca',
        'https://www.bad234123421342134.com',
        'https://www.tmall.com',
        'https://tmxmoney.com/en/index.html',
    ]
    for u in url_array:
        print(fu.download_url(u)[:50])


def _main():
    demo_commission()
    demo_fu()


if __name__ == '__main__':
    _main()
