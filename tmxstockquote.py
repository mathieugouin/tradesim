"""TMX Stock Quote module provides a Python API for retrieving stock data from TMX."""

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


def _yahoo_to_tmx_stock_name(symbol):
    """Convert yahoo style stock quote to TMX style."""
    m = re.match(r"(\S+?)\.TO", symbol, re.IGNORECASE)
    if m:
        tmx_name = m.group(1)
    else:
        tmx_name = symbol + ":US"

    return tmx_name.replace("-", ".")


def _download_tmx_page(symbol):
    """Download the TMX data page for a given symbol.  A caching is implemented to prevent multiple re-download."""
    global _cached_symbol
    global _cached_lines

    symbol = _yahoo_to_tmx_stock_name(symbol)
    url = "https://web.tmxmoney.com/quote.php?qm_symbol=" + symbol

    if _cached_symbol and _cached_symbol == symbol:
        lines = _cached_lines
    else:
        lines = fu.download_url(url).splitlines()
        _cached_symbol = symbol
        _cached_lines = lines

    return lines


def _request_tmx_re(symbol, re_str):
    """With a single re string, scan through all lines of the symbol page."""
    value = ""
    lines = _download_tmx_page(symbol)
    for line in lines:
        m = re.search(re_str, line)
        if m:
            value = m.group(1)
            break

    return value


def _request_tmx_multi_re(symbol, re_arr):
    """Scan using an array of re str, starting from the 1st element.  The last element must be the match."""
    value = ""
    lines = _download_tmx_page(symbol)
    if len(re_arr) > 0:
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


def _request_tmx_str(symbol, stat):
    """Default TMX card display grabber (string return)."""
    re_arr = [
        re.escape('<div class="dq-card">'),
        re.escape(stat),
        re.escape('<strong>') + '(.*?)' + re.escape('</strong>')
    ]

    return _request_tmx_multi_re(symbol, re_arr)


def _request_tmx(symbol, stat):
    """Default TMX card display grabber (float return)."""
    return _str_to_float(_request_tmx_str(symbol, stat))


def get_name(symbol):
    """Full company name from symbol."""
    re_str = re.escape('<h4>') + '(.*?)' + re.escape('</h4>')
    return _request_tmx_re(symbol, re_str)


def get_volume(symbol):
    """Current day's trading volume in number of shares."""
    re_arr = [
        '\\b' + re.escape('VOLUME<br />'),
        '\\<strong.*?(-?[0-9 ,.]{1,})'
    ]
    return _str_to_float(_request_tmx_multi_re(symbol, re_arr))


def get_price(symbol):
    """Current day's trading last price."""
    return _str_to_float(_request_tmx_re(symbol, r'\$\s+<span>([0-9\., ]+)</span>'))


def get_change(symbol):
    """Change in $ for the day."""
    re_arr = [
        '\\b' + re.escape('CHANGE<br />'),
        '\\<strong.*?(-?[0-9 ,.]{3,})'
    ]
    return _str_to_float(_request_tmx_multi_re(symbol, re_arr))


def get_stock_exchange(symbol):
    """Return the name of the stock exchange the stock is traded."""
    re_arr = [
        re.escape('<p class="blurb text-darkgrey"><strong class="text-darkgrey">'),
        r'\s*(.+?) <\/strong> \|'
    ]
    return _request_tmx_multi_re(symbol, re_arr)


def get_52_week_high(symbol):
    """Highest price value during the last 52 weeks."""
    return _str_to_float(_request_tmx_re(symbol, '<strong>52 Week High:</strong></a>\\s*(.+?)</div>'))


def get_52_week_low(symbol):
    """Lowest price value during the last 52 weeks."""
    re_arr = [
        '<strong>52 Week Low:</strong></a>',
        '\\s*(.+?)</div>'
    ]
    return _str_to_float(_request_tmx_multi_re(symbol, re_arr))


def get_currency(symbol):
    """Currency the stock trades in.  Quick implementation based on the ticker."""
    if _yahoo_to_tmx_stock_name(symbol).endswith(':US'):
        return 'USD'
    return 'CAD'


def get_market_cap(symbol):
    """Return the market capitalization of the given stock."""
    return _request_tmx(symbol, "Market Cap<sup>1</sup>:")


def get_dividend_yield(symbol):
    """Return the divident yield of the stock."""
    return _request_tmx(symbol, "Yield:")


def get_price_earnings_ratio(symbol):
    """Return the P/E ratio."""
    return _request_tmx(symbol, "P/E Ratio:")


def get_price_book_ratio(symbol):
    """Return the P/B ratio."""
    return _request_tmx(symbol, "P/B Ratio:")
