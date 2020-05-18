import math
import tmxstockquote as tmx
import pytest


@pytest.mark.parametrize('s,n', [
    ('0', 0),
    ('34.50', 34.5),
    ('-34.50', -34.5),
    ('1,300,400.52', 1300400.52),
    ('-1,300,400.52', -1300400.52),
])
def test_tmx_internal_str_good(s, n):
    assert tmx._str_to_float(s) == n


@pytest.mark.parametrize('s', [
    '',
    'bad number',
    'n/a',
    'N/A',
    'null',
    'NULL',
])
def test_tmx_internal_str_nan(s):
    assert math.isnan(tmx._str_to_float(s))


@pytest.mark.parametrize("y,t", [
    ('CP.TO', 'CP'),
    ('AP-UN.TO', 'AP.UN'),
    ('MMM', 'MMM:US'),
])
def test_tmx_internal_conv(y, t):
    assert tmx._yahoo_to_tmx_stock_name(y) == t


@pytest.mark.webtest
def test_tmx_internal_dl():
    assert len(tmx._download_tmx_page('XBB.TO')) > 100


@pytest.mark.webtest
def test_tmx_internal_re():
    assert len(tmx._request_tmx_multi_re('XBB.TO', [])) == 0


@pytest.mark.webtest
@pytest.mark.parametrize("s", ['NA.TO', 'XBB.TO', 'AP-UN.TO', 'BITF.TO', 'AAPL', 'XOM'])
def test_tmx_api_common(s):
    assert len(tmx.get_name(s)) > 0
    assert tmx.get_price(s) > 0
    assert -1000 < tmx.get_change(s) < 1000
    assert tmx.get_volume(s) > 0
    assert len(tmx.get_stock_exchange(s)) > 5
    assert tmx.get_market_cap(s) > 0
    assert tmx.get_52_week_low(s) > 0
    assert tmx.get_52_week_high(s) > 0
    c = tmx.get_currency(s)
    assert c == 'USD' or c == 'CAD'


@pytest.mark.webtest
@pytest.mark.parametrize("s", ['XBB.TO', 'NA.TO', 'SPY', 'XOM'])
def test_tmx_api_dividend(s):
    assert 0 <= tmx.get_dividend_yield(s) < 100


@pytest.mark.webtest
@pytest.mark.parametrize("s", ['NA.TO', 'AAPL'])
def test_tmx_api_company(s):
    assert 0 <= tmx.get_price_earnings_ratio(s) < 100
    assert 0 <= tmx.get_price_book_ratio(s) < 100
