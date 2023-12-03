import math
import pytest
import ystockquote as ysq

pytest.skip("Skipping unstable ystockquote tests", allow_module_level=True)


@pytest.mark.webtest
@pytest.mark.parametrize("i", ['', 'badInfo', 'volume ', ' volume'])
def test_get_info(i):
    s = 'IBM'
    assert ysq._get_info(s, i) is None


@pytest.mark.webtest
def test_get_info_choice():
    s = 'IBM'
    assert ysq._get_info_choice(s, []) is None


@pytest.mark.webtest
@pytest.mark.parametrize("api", [
        'get_price',
        'get_volume',
        'get_market_cap',
        'get_52_week_low',
        'get_52_week_high'
    ])
@pytest.mark.parametrize("s", [
        'NA.TO',
        'XBB.TO',
        'AP-UN.TO',
        'AAPL',
        'XOM',
        'BRK-A',
        'SPY'
    ])
def test_ysq_api_common(s, api):
    assert not math.isnan(getattr(ysq, api)(s))


@pytest.mark.webtest
@pytest.mark.parametrize("s", ['NA.TO', 'XBB.TO', 'AP-UN.TO', 'AAPL', 'XOM'])
def test_ysq_get_name(s):
    assert len(ysq.get_name(s)) > 5


@pytest.mark.webtest
@pytest.mark.parametrize("s", ['NA.TO', 'XBB.TO', 'AAPL', 'XOM'])
def test_ysq_get_stock_exchange(s):
    assert len(ysq.get_stock_exchange(s)) > 2


@pytest.mark.webtest
@pytest.mark.parametrize("s", ['NA.TO', 'XBB.TO', 'AAPL', 'XOM'])
def test_ysq_get_currency(s):
    c = ysq.get_currency(s)
    assert c in ['USD', 'CAD']


@pytest.mark.webtest
@pytest.mark.parametrize("s", ['XBB.TO', 'VUN.TO', 'ZCN.TO', 'BMO.TO', 'SPY', 'XOM', 'TSLA'])
def test_ysq_api_dividend(s):
    assert 0 <= ysq.get_dividend_yield(s) < 100


@pytest.mark.webtest
@pytest.mark.parametrize("s", ['NA.TO', 'AAPL', 'IBM'])
def test_ysq_get_price_earnings_ratio(s):
    assert 0 <= ysq.get_price_earnings_ratio(s) < 100
