"""Yahoo Stock Quote module provides a Python API for retrieving stock data from Yahoo."""

import finance_utils as fu
import re

_cached_symbol = None
_cached_lines = None


def _str_to_float(s):
    """Convert a string into float, returns NaN, when not a number."""
    try:
        return float(s.replace(",", "").replace(" ", ""))
    except Exception:
        return float('nan')


def _download_page(symbol):
    """Download the Yahoo data page for a given symbol.  A caching is implemented to prevent multiple re-download."""
    global _cached_symbol
    global _cached_lines

    url = "https://finance.yahoo.com/quote/" + symbol

    if _cached_symbol and _cached_symbol == symbol:
        lines = _cached_lines
    else:
        lines = fu.download_url(url).splitlines()
        _cached_symbol = symbol
        _cached_lines = lines

    return lines


def _request_re(symbol, re_str):
    """With a single re string, scan through all lines of the symbol page."""
    value = ""
    lines = _download_page(symbol)
    for line in lines:
        m = re.search(re_str, line)
        if m:
            value = m.group(1)
            break

    return value


def _request_multi_re(symbol, re_arr):
    """Scan using an array of re str, starting from the 1st element.  The last element must be the match."""
    value = ""
    if len(re_arr) > 0:
        lines = _download_page(symbol)
        j = 0  # re_arr indexer
        for line in lines:
            m = re.search(re_arr[j], line)
            if m:
                # If we are at the last re
                if j == len(re_arr) - 1:
                    value = m.group(1)
                    break
                # continue at next re
                j = j + 1
    return value


def _request_str(symbol, stat):
    """Default TMX card display grabber (string return)."""
    re_arr = [
        re.escape('<div class="dq-card">'),
        re.escape(stat),
        re.escape('<strong>') + '(.*?)' + re.escape('</strong>')
    ]

    return _request_multi_re(symbol, re_arr)


def _request_ysq(symbol, stat):
    """Default TMX card display grabber (float return)."""
    return _str_to_float(_request_str(symbol, stat))


def get_name(symbol):
    """Full company name from symbol."""
    re_str = re.escape('<h1 class="D(ib) Fz(18px)" data-reactid="7">') + '(.+?)' + re.escape('</h1>')
    result = _request_re(symbol, re_str)
    result = result.replace(' (' + symbol + ')', '')
    return result


def get_volume(symbol):
    """Current day's trading volume in number of shares."""

    # data-test="TD_VOLUME-value" data-reactid="69"><span class="Trsdu(0.3s) " data-reactid="70">35,953</span></td></tr>
    # data-test="TD_VOLUME-value" data-reactid="115"><span class="Trsdu(0.3s) " data-reactid="116">273,818</span></td>
    return _str_to_float(
        _request_re(
            symbol,
            re.escape('data-test="TD_VOLUME-value" data-reactid="') +
            '\d+' +
            re.escape('"><span class="Trsdu(0.3s) " data-reactid="') +
            '\d+' +
            re.escape('">') +
            '(.+?)' +
            re.escape('</span></td></tr>')))


def get_price(symbol):
    """Current day's trading last price."""
    return _str_to_float(
        _request_re(
            symbol,
            re.escape('<span class="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)" data-reactid="32">') +
            '(.+?)' +
            re.escape('</span>')))


def get_change(symbol):
    """Change in $ for the day."""
    # <span class="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor)" data-reactid="33">-0.10 (-0.15%)</span>
    # <span class="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)" data-reactid="33">+0.02 (+0.07%)</span>
    # <span class="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px)" data-reactid="33">0.00 (0.00%)</span>

    return _str_to_float(
        _request_re(
            symbol,
            re.escape('<span class="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px)') +
            '(?: C\(\$(?:negative|positive)Color\))?' +
            re.escape('" data-reactid="33">') +
            '(.+?) \(.+?\)' +
            re.escape('</span>')))


def get_stock_exchange(symbol):
    """Return the name of the stock exchange the stock is traded."""
    re_arr = [
        re.escape('<p class="blurb text-darkgrey"><strong class="text-darkgrey">'),
        r'\s*(.+?) <\/strong> \|'
    ]
    return _request_multi_re(symbol, re_arr)


def get_52_week_high(symbol):
    """Highest price value during the last 52 weeks."""
    return _str_to_float(_request_re(symbol, '<strong>52 Week High:</strong></a>\\s*(.+?)</div>'))


def get_52_week_low(symbol):
    """Lowest price value during the last 52 weeks."""
    re_arr = [
        '<strong>52 Week Low:</strong></a>',
        '\\s*(.+?)</div>'
    ]
    return _str_to_float(_request_multi_re(symbol, re_arr))


def get_currency(symbol):
    """Currency the stock trades in.  Quick implementation based on the ticker."""
    if symbol.endswith('.TO'):
        return 'CAD'
    return 'USD'


def get_market_cap(symbol):
    """Return the market capitalization of the given stock."""
    # data-test="MARKET_CAP-value" data-reactid="128"><span class="Trsdu(0.3s) " data-reactid="129">22.793B</span></td>
    s = _request_re(
            symbol,
            re.escape('data-test="') +
            '(?:MARKET_CAP|NET_ASSETS)' +
            re.escape('-value" data-reactid="') +
            '\d+' +
            re.escape('"><span class="Trsdu(0.3s) " data-reactid="') +
            '\d+' +
            re.escape('">') +
            '(.+?)' +
            re.escape('</span></td></tr>'))
    if s.endswith('T'):
        return _str_to_float(s[:-1]) * 1000000000000
    if s.endswith('B'):
        return _str_to_float(s[:-1]) * 1000000000
    elif s.endswith('M'):
        return _str_to_float(s[:-1]) * 1000000
    else:
        return _str_to_float(s)


def get_dividend_yield(symbol):
    """Return the dividend yield (in %) of the stock."""
    return _request_ysq(symbol, "Yield:")


def get_price_earnings_ratio(symbol):
    """Return the P/E ratio."""
    return _request_ysq(symbol, "P/E Ratio:")


def get_price_book_ratio(symbol):
    """Return the P/B ratio."""
    return _request_ysq(symbol, "P/B Ratio:")
