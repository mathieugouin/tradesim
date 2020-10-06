# To make print working for Python2/3
from __future__ import print_function

import ystockquote as ysq


def _main():

    print(ysq._str_to_float("34.50"))
    print(ysq._str_to_float("1,300,400.52"))
    print(ysq._str_to_float(""))
    print(ysq._str_to_float("N/A"))
    print("")

    print(ysq._download_page('XBB.TO')[0][0:80])
    print("")

    for s in ["NA.TO", "XBB.TO", "AP-UN.TO", "BRK-A", "AAPL"]:
        print("=============================================")
        print("s: {}".format(s))

        print("get_name: {}".format(ysq.get_name(s)))
        print("get_price: {}".format(ysq.get_price(s)))
        print("get_change: {}".format(ysq.get_change(s)))
        print("get_volume: {}".format(ysq.get_volume(s)))
        print("get_stock_exchange: {}".format(ysq.get_stock_exchange(s)))
        print("get_market_cap: {}".format(ysq.get_market_cap(s)))
        print("get_dividend_yield: {}".format(ysq.get_dividend_yield(s)))
        print("get_price_earnings_ratio: {}".format(ysq.get_price_earnings_ratio(s)))
        print("get_price_book_ratio: {}".format(ysq.get_price_book_ratio(s)))

        print("get_52_week_low: {}".format(ysq.get_52_week_low(s)))
        print("get_52_week_high: {}".format(ysq.get_52_week_high(s)))
        print("get_currency: {}".format(ysq.get_currency(s)))


if __name__ == '__main__':
    _main()
