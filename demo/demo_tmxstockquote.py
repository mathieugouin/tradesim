# To make print working for Python2/3
from __future__ import print_function

import tmxstockquote as tsx


def _main():
    print(tsx._str_to_float("34.50"))
    print(tsx._str_to_float("1,300,400.52"))
    print(tsx._str_to_float(""))
    print(tsx._str_to_float("N/A"))
    print("")

    print(tsx._yahoo_to_tmx_stock_name("CP.TO"))
    print(tsx._yahoo_to_tmx_stock_name("AP-UN.TO"))
    print(tsx._yahoo_to_tmx_stock_name("MMM"))
    print("")

    print(tsx._download_tmx_page('XBB.TO')[0:2])
    print("")

    for s in ["NA.TO", "XBB.TO", "AP-UN.TO", "BRK-A", "AAPL"]:
        print("=============================================")
        print("s: {}".format(s))

        print("get_name: {}".format(tsx.get_name(s)))
        print("get_price: {}".format(tsx.get_price(s)))
        print("get_change: {}".format(tsx.get_change(s)))
        print("get_volume: {}".format(tsx.get_volume(s)))
        print("get_stock_exchange: {}".format(tsx.get_stock_exchange(s)))
        print("get_market_cap: {}".format(tsx.get_market_cap(s)))
        print("get_dividend_yield: {}".format(tsx.get_dividend_yield(s)))
        print("get_price_earnings_ratio: {}".format(tsx.get_price_earnings_ratio(s)))
        print("get_price_book_ratio: {}".format(tsx.get_price_book_ratio(s)))

        print("get_52_week_low: {}".format(tsx.get_52_week_low(s)))
        print("get_52_week_high: {}".format(tsx.get_52_week_high(s)))
        print("get_currency: {}".format(tsx.get_currency(s)))


if __name__ == '__main__':
    _main()
