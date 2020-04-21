import tmxstockquote as tsx


def test_tmx():
    # assert tsx._str_to_float('34.50') == 34.5
    # assert tsx._str_to_float('1,300,400.52') == 1300400.52
    # assert tsx._str_to_float('') == float('nan')
    # assert tsx._str_to_float('bad number') == float('nan')
    # assert tsx._str_to_float('N/A') == float('nan')
    # assert tsx._str_to_float('null') == float('nan')

    # assert tsx._yahoo_to_tmx_stock_name('CP.TO') == 'CP'
    # assert tsx._yahoo_to_tmx_stock_name('AP-UN.TO') == 'AP.UN'
    # assert tsx._yahoo_to_tmx_stock_name('MMM') == 'MMM:US'

    # assert len(tsx._download_tmx_page('XBB.TO')) > 100

    for s in ['NA.TO', 'XBB.TO', 'BRK-A', 'AAPL']:
        assert len(tsx.get_name(s)) > 0
        assert tsx.get_price(s) > 0
        # print('get_change: {}'.format(tsx.get_change(s)))
        # print('get_volume: {}'.format(tsx.get_volume(s)))
        # print('get_stock_exchange: {}'.format(tsx.get_stock_exchange(s)))
        # print('get_market_cap: {}'.format(tsx.get_market_cap(s)))
        # print('get_dividend_yield: {}'.format(tsx.get_dividend_yield(s)))
        # print('get_price_earnings_ratio: {}'.format(tsx.get_price_earnings_ratio(s)))
        # print('get_price_book_ratio: {}'.format(tsx.get_price_book_ratio(s)))

        # print('get_52_week_low: {}'.format(tsx.get_52_week_low(s)))
        # print('get_52_week_high: {}'.format(tsx.get_52_week_high(s)))
        # print('get_currency: {}'.format(tsx.get_currency(s)))
