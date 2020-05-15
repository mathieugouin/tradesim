import math
import tmxstockquote as tsx
import pytest


def test_tmx_internal_str():
    assert tsx._str_to_float('34.50') == 34.5
    assert tsx._str_to_float('1,300,400.52') == 1300400.52
    assert math.isnan(tsx._str_to_float(''))
    assert math.isnan(tsx._str_to_float('bad number'))
    assert math.isnan(tsx._str_to_float('N/A'))
    assert math.isnan(tsx._str_to_float('null'))


def test_tmx_internal_conv():
    assert tsx._yahoo_to_tmx_stock_name('CP.TO') == 'CP'
    assert tsx._yahoo_to_tmx_stock_name('AP-UN.TO') == 'AP.UN'
    assert tsx._yahoo_to_tmx_stock_name('MMM') == 'MMM:US'


@pytest.mark.webtest
def test_tmx_internal_dl():
    assert len(tsx._download_tmx_page('XBB.TO')) > 100


@pytest.mark.webtest
def test_tmx_internal_re():
    assert len(tsx._request_tmx_multi_re('XBB.TO', [])) == 0


@pytest.mark.webtest
@pytest.mark.parametrize("s", ['NA.TO', 'XBB.TO', 'AP-UN.TO', 'BITF.TO', 'AAPL', 'XOM'])
def test_tmx_api_common(s):
    assert len(tsx.get_name(s)) > 0
    assert tsx.get_price(s) > 0
    assert -1000 < tsx.get_change(s) < 1000
    assert tsx.get_volume(s) > 0
    assert len(tsx.get_stock_exchange(s)) > 5
    assert tsx.get_market_cap(s) > 0
    assert tsx.get_52_week_low(s) > 0
    assert tsx.get_52_week_high(s) > 0
    c = tsx.get_currency(s)
    assert c == 'USD' or c == 'CAD'


@pytest.mark.webtest
def test_tmx_api_dividend():
    s = 'XBB.TO'
    assert 0 <= tsx.get_dividend_yield(s) < 100


@pytest.mark.webtest
def test_tmx_api_company():
    for s in ['NA.TO', 'AAPL']:
        assert 0 <= tsx.get_price_earnings_ratio(s) < 100
        assert 0 <= tsx.get_price_book_ratio(s) < 100
