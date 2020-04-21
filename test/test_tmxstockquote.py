import tmxstockquote as tsx


def test_tmx():
    # print(tsx._str_to_float("34.50"))
    # print(tsx._str_to_float("1,300,400.52"))
    # print(tsx._str_to_float(""))
    # print(tsx._str_to_float("N/A"))

    # print(tsx._yahoo_to_tmx_stock_name("CP.TO"))
    # print(tsx._yahoo_to_tmx_stock_name("AP-UN.TO"))
    # print(tsx._yahoo_to_tmx_stock_name("MMM"))

    # print(tsx._download_tmx_page('XBB.TO')[0:2])

    for s in ["NA.TO", "XBB.TO", "BRK-A", "AAPL"]:
        assert len(tsx.get_name(s)) > 0
        assert len(tsx.get_price(s)) > 0
        # print("get_change: {}".format(tsx.get_change(s)))
        # print("get_volume: {}".format(tsx.get_volume(s)))
        # print("get_stock_exchange: {}".format(tsx.get_stock_exchange(s)))
        # print("get_market_cap: {}".format(tsx.get_market_cap(s)))
        # print("get_dividend_yield: {}".format(tsx.get_dividend_yield(s)))
        # print("get_price_earnings_ratio: {}".format(tsx.get_price_earnings_ratio(s)))
        # print("get_price_book_ratio: {}".format(tsx.get_price_book_ratio(s)))

        # print("get_52_week_low: {}".format(tsx.get_52_week_low(s)))
        # print("get_52_week_high: {}".format(tsx.get_52_week_high(s)))
        # print("get_currency: {}".format(tsx.get_currency(s)))
