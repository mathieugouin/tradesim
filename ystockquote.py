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

    if _cached_symbol and _cached_symbol == symbol:
        lines = _cached_lines
    else:
        url = "https://finance.yahoo.com/quote/" + symbol
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
            re.escape('<span class="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)" data-reactid=') + 
            '"\d+">(.+?)' +
            re.escape('</span>')))


def get_change(symbol):
    """Change in $ for the day."""
    # <span class="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor)" data-reactid="33">-0.10 (-0.15%)</span>
    # <span class="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)" data-reactid="33">+0.02 (+0.07%)</span>
    # <span class="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px)" data-reactid="33">0.00 (0.00%)</span>
    # <span class="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor)" data-reactid="34">-0.41 (-0.57%)</span>
    return _str_to_float(
        _request_re(
            symbol,
            re.escape('<span class="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px)') +
            '(?: C\(\$(?:negative|positive)Color\))?' +
            re.escape('" data-reactid="') + 
            "\d+" +
            re.escape('">') +
            '(.+?) \(.+?\)' +
            re.escape('</span>')))


def get_stock_exchange(symbol):
    """Return the name of the stock exchange the stock is traded."""
    # <div class="C($tertiaryColor) Fz(12px)" data-reactid="8"><span data-reactid="9">NasdaqGS - NasdaqGS Real Time Price. Currency in USD</span></div>
    # <div class="C($tertiaryColor) Fz(12px)" data-reactid="8"><span data-reactid="9">NYSE - NYSE Delayed Price. Currency in USD</span></div>
    # <div class="C($tertiaryColor) Fz(12px)" data-reactid="8"><span data-reactid="9">Toronto - Toronto Real Time Price. Currency in CAD</span></div>
    # <div class="C($tertiaryColor) Fz(12px)" data-reactid="8"><span data-reactid="9">TSXV - TSXV Real Time Price. Currency in CAD</span></div>
    return _request_re(symbol, '<span data-reactid="\d+">(.+?) - .*?Currency in (?:USD|CAD)<\/span>')



def get_52_week_high(symbol):
    """Highest price value during the last 52 weeks."""
    # <td class="Ta(end) Fw(600) Lh(14px)" data-test="FIFTY_TWO_WK_RANGE-value" data-reactid="65">28.58 - 34.39</td>
    s = _request_re(symbol, 'data-test="FIFTY_TWO_WK_RANGE-value" data-reactid="\d+"\>(.+?)\<\/td\>')
    m = re.search('^(.+?) - (.+?)$', s)
    if m:
        return _str_to_float(m.group(2))
    return _str_to_float('nan')

def get_52_week_low(symbol):
    # <td class="Ta(end) Fw(600) Lh(14px)" data-test="FIFTY_TWO_WK_RANGE-value" data-reactid="65">28.58 - 34.39</td>
    """Lowest price value during the last 52 weeks."""
    s = _request_re(symbol, 'data-test="FIFTY_TWO_WK_RANGE-value" data-reactid="\d+"\>(.+?)\<\/td\>')
    m = re.search('^(.+?) - (.+?)$', s)
    if m:
        return _str_to_float(m.group(1))
    return _str_to_float('nan')


def get_currency(symbol):
    """Currency the stock trades in.  Quick implementation based on the ticker."""
    # <span data-reactid="9">NasdaqGS - NasdaqGS Real Time Price. Currency in USD</span>
    return _request_re(symbol, '<span data-reactid="\d+">.+?Currency in (USD|CAD)<\/span>')


def get_market_cap(symbol):
    """Return the market capitalization of the given stock."""
    # data-test="MARKET_CAP-value" data-reactid="128"><span class="Trsdu(0.3s) " data-reactid="129">22.793B</span></td>
    # data-test="NET_ASSETS-value" data-reactid="82"><span class="Trsdu(0.3s) " data-reactid="83">4.83B</span></td>
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
    elif s.endswith('B'):
        return _str_to_float(s[:-1]) * 1000000000
    elif s.endswith('M'):
        return _str_to_float(s[:-1]) * 1000000
    else:
        return _str_to_float(s)


def get_dividend_yield(symbol):
    """Return the dividend yield (in %) of the stock."""
    # https://finance.yahoo.com/quote/CM.TO: 5.84 (5.75%)
    # data-test="DIVIDEND_AND_YIELD-value" data-reactid="153">4.32 (4.44%)</td>
    # https://finance.yahoo.com/quote/XBB.TO: 2.60%
    # data-test="TD_YIELD-value" data-reactid="97"><span class="Trsdu(0.3s) " data-reactid="98">5.34%</span></td>
    # data-test="TD_YIELD-value" data-reactid="99"><span class="Trsdu(0.3s) " data-reactid="100">1.69%</span></td>
    return _str_to_float(
        _request_re(
            symbol,
            'data-test="(?:DIVIDEND_AND_YIELD|TD_YIELD)-value" data-reactid="\d+">.+?(?:\d+\.\d+ )?(\d+\.\d+)%.*?<\/td>'))


def get_price_earnings_ratio(symbol):
    """Return the P/E ratio."""
    # <td class="Ta(end) Fw(600) Lh(14px)" data-test="PE_RATIO-value" data-reactid="138"><span class="Trsdu(0.3s) " data-reactid="139">11.81</span></td>
    return _str_to_float(
        _request_re(
            symbol,
            re.escape('data-test="PE_RATIO-value" data-reactid="') +
            '\d+' +
            re.escape('"><span class="Trsdu(0.3s) " data-reactid="') +
            '\d+' +
            re.escape('">') +
            '(.+?)' +
            re.escape('</span></td></tr>')))
