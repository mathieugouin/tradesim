import parent_import
import ystockquote as ysq


def _main():

    for s in ["NA.TO", "XBB.TO", "NOU.V", "AP-UN.TO", "BRK-A", "AAPL", "SPY"]:
        print("=============================================")
        print("s: {}".format(s))

        print("get_name: {}".format(ysq.get_name(s)))
        print("get_price: {}".format(ysq.get_price(s)))
        print("get_volume: {}".format(ysq.get_volume(s)))
        print("get_stock_exchange: {}".format(ysq.get_stock_exchange(s)))
        print("get_market_cap: {}".format(ysq.get_market_cap(s)))
        print("get_dividend_yield: {}".format(ysq.get_dividend_yield(s)))
        print("get_price_earnings_ratio: {}".format(ysq.get_price_earnings_ratio(s)))

        print("get_52_week_low: {}".format(ysq.get_52_week_low(s)))
        print("get_52_week_high: {}".format(ysq.get_52_week_high(s)))
        print("get_currency: {}".format(ysq.get_currency(s)))


if __name__ == '__main__':
    _main()
