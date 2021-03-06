# To make print working for Python2/3
from __future__ import print_function

import datetime
import numpy as np
import finance_utils as fu


def _main():
    sf = '../stock_db/dj.txt'
    print("symbol file {} contains the following stocks: {}".format(sf, fu.get_symbols_from_file(sf)))

    d = '../stock_db/test'

    s = 'SPY'
    f = fu.symbol_to_filename(s, d)
    print("symbol {} with directory {} gives filename {}".format(s, d, f))
    print("filename {} gives symbol {}".format(f, fu.filename_to_symbol(f)))
    print("filename {} gives symbol {}".format(f.upper(), fu.filename_to_symbol(f.upper())))
    print("validate_symbol_data {} = {}".format(f, fu.validate_symbol_data(f)))

    print("directory {} contains the following stocks: {}".format(d, fu.get_all_symbols(d)))

    start_date = datetime.date(1900, 1, 1)
    end_date = datetime.date.today()

    if False:
        fu.download_data(s, d, start_date, end_date)
        fu.update_all_symbols(d, start_date, end_date)
    df = fu.load_data_frame(f, datetime.date(2018, 1, 1), datetime.date(2018, 4, 1))
    print(df.describe())
    print(df.head())

    print(fu.get_date(df)[0:3])
    print(fu.get_open(df)[0:3])
    print(fu.get_high(df)[0:3])
    print(fu.get_low(df)[0:3])
    print(fu.get_close(df)[0:3])
    print(fu.get_volume(df)[0:3])

    # Not applicable for a single stock, but just to test...
    print(fu.normalize_data_frame(df).head())

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


if __name__ == '__main__':
    _main()
