# To make print working for Python2/3
from __future__ import print_function

import tmxstockquote as tsq


def _main():
    print(tsq._str_to_float("34.50"))
    print(tsq._str_to_float("1,300,400.52"))
    print(tsq._str_to_float(""))
    print(tsq._str_to_float("N/A"))
    print("")

    print(tsq._yahoo_to_tmx_stock_name("CP.TO"))
    print(tsq._yahoo_to_tmx_stock_name("AP-UN.TO"))
    print(tsq._yahoo_to_tmx_stock_name("MMM"))
    print("")

    print(tsq._download_tmx_page('XBB.TO')[0:2])
    print("")

    for s in ["NA.TO", "XBB.TO", "BRK-A", "AAPL"]:
        print("=============================================")
        print("s: {}".format(s))

        print("get_name: {}".format(tsq.get_name(s)))
        print("get_price: {}".format(tsq.get_price(s)))
        print("get_change: {}".format(tsq.get_change(s)))
        print("get_volume: {}".format(tsq.get_volume(s)))
        print("get_stock_exchange: {}".format(tsq.get_stock_exchange(s)))
        print("get_market_cap: {}".format(tsq.get_market_cap(s)))
        print("get_dividend_yield: {}".format(tsq.get_dividend_yield(s)))
        print("get_price_earnings_ratio: {}".format(tsq.get_price_earnings_ratio(s)))
        print("get_price_book_ratio: {}".format(tsq.get_price_book_ratio(s)))

        print("get_52_week_low: {}".format(tsq.get_52_week_low(s)))
        print("get_52_week_high: {}".format(tsq.get_52_week_high(s)))
        print("get_currency: {}".format(tsq.get_currency(s)))


if __name__ == '__main__':
    _main()
