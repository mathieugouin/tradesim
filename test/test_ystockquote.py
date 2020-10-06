import math
import ystockquote as ysq
import pytest


@pytest.mark.parametrize('s,n', [
    ('0', 0),
    ('34.50', 34.5),
    ('-34.50', -34.5),
    ('1,300,400.52', 1300400.52),
    ('-1,300,400.52', -1300400.52),
])
def test_ysq_internal_str_good(s, n):
    assert ysq._str_to_float(s) == n


@pytest.mark.parametrize('s', [
    '',
    'bad number',
    'n/a',
    'N/A',
    'null',
    'NULL',
])
def test_ysq_internal_str_nan(s):
    assert math.isnan(ysq._str_to_float(s))


@pytest.mark.webtest
def test_ysq_internal_dl():
    assert len(ysq._download_page('XBB.TO')) > 100


@pytest.mark.webtest
def test_ysq_internal_re():
    assert len(ysq._request_multi_re('XBB.TO', [])) == 0


@pytest.mark.webtest
@pytest.mark.parametrize("api", ['get_price', 'get_change', 'get_volume', 'get_market_cap', 'get_52_week_low', 'get_52_week_high'])
@pytest.mark.parametrize("s", ['NA.TO', 'XBB.TO', 'AP-UN.TO', 'BITF.TO', 'AAPL', 'XOM'])
def test_ysq_api_common(s, api):
    assert not math.isnan(getattr(ysq, api)(s))


@pytest.mark.webtest
@pytest.mark.parametrize("s", ['NA.TO', 'XBB.TO', 'AP-UN.TO', 'BITF.TO', 'AAPL', 'XOM'])
def test_ysq_api_special(s):
    assert len(ysq.get_name(s)) > 0
    assert len(ysq.get_stock_exchange(s)) > 5
    c = ysq.get_currency(s)
    assert c == 'USD' or c == 'CAD'


@pytest.mark.webtest
@pytest.mark.parametrize("s", ['XBB.TO', 'NA.TO', 'SPY', 'XOM'])
def test_ysq_api_dividend(s):
    assert 0 <= ysq.get_dividend_yield(s) < 100


@pytest.mark.webtest
@pytest.mark.parametrize("s", ['NA.TO', 'AAPL'])
def test_ysq_api_company(s):
    assert 0 <= ysq.get_price_earnings_ratio(s) < 100
    assert 0 <= ysq.get_price_book_ratio(s) < 100
