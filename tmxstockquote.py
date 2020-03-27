#!/usr/bin/env python

import urllib
import re
import time
import math


"""
This module provides a Python API for retrieving stock data from TMX
"""

_cached_symbol = None
_cached_lines = None


def _str_to_float(s):
    try:
        return float(s.replace(",", "").replace(" ", ""))
    except Exception as e:
        return 0.0


def _yahoo_to_tmx_stock_name(symbol):
    """Convert yahoo style stock quote to TMX style."""
    tmx_name = ""
    m = re.match("(\S+?)\.TO", symbol, re.IGNORECASE)
    if (m):
        tmx_name = m.group(1)
    else:
        tmx_name = symbol + ":US"

    return tmx_name.replace("-", ".")


def _get_url(url):
    """Download a URL and provide the result as a big string."""
    try_again = True
    count = 0
    s = ""
    while try_again and count < 5:
        try:
            s = urllib.urlopen(url).read().strip()
            try_again = False
        except:
            print "Error, will try again"
            time.sleep(0.5)  # 500 ms sleep
            count += 1
    return s


def _download_tmx_page(symbol):
    """Download the TMX data page for a given symbol.  A caching is implemented to prevent multiple re-download."""
    global _cached_symbol
    global _cached_lines

    symbol = _yahoo_to_tmx_stock_name(symbol)
    url = "https://web.tmxmoney.com/quote.php?qm_symbol=" + symbol

    if _cached_symbol and _cached_symbol == symbol:
        lines = _cached_lines
    else:
        lines = _get_url(url).splitlines()
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
                else:
                    j = j + 1  # continue at next re
    return value


def _request_tmx_str(symbol, stat):
    """Default TMX card display grabber (string return)"""
    re_str = re.escape(r'<td> <span class="l">') + \
             re.escape(stat) + \
             re.escape(r'</span></td><td> <span class="dt">') + '(.*?)' + \
             re.escape(r'</span></td>')

    return _request_tmx_re(symbol, re_str)


def _request_tmx(symbol, stat):
    """Default TMX card display grabber (float return)"""
    return _str_to_float(_request_tmx_str(symbol, stat))


def get_company_name(symbol):
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
    return _str_to_float(_request_tmx_re(symbol, '\\$\\s+<span>([0-9\., ]+)</span>'))


def get_change(symbol):
    """Change in $ for the day"""
    re_arr = [
        '\\b' + re.escape('CHANGE<br />'),
        '\\<strong.*?(-?[0-9 ,.]{3,})'
    ]
    return _str_to_float(_request_tmx_multi_re(symbol, re_arr))


def get_stock_exchange(symbol):
    re_arr = [
        re.escape('<p class="blurb text-darkgrey"><strong class="text-darkgrey">'),
        '\\s*(.+?) <\/strong> \|'
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
    """TBD Not implemented"""
    return "N/A"


# Test Indicator ##############################
# def relative_position(symbol):
#     price = get_price(symbol)
#     pmin = get_52_week_low(symbol)
#     pmax = get_52_week_high(symbol)
#
#     return (price - pmin) / (pmax - pmin)
#
#
# def relative_range(symbol):
#     pmin = get_52_week_low(symbol)
#     pmax = get_52_week_high(symbol)
#
#     return (pmax - pmin) / pmax
#
#
# def test_indicator(symbol):
#     # [-1, 1]
#     rps = relative_position(symbol) * 2.0 - 1.0
#
#     # [0, 1]
#     rr = relative_range(symbol)
#
#     # reduce the rr influence
#     return rps * math.pow(rr, 0.1)


def _main():
    print _str_to_float("34.50")
    print _str_to_float("1,300,400.52")
    print _str_to_float("")
    print _str_to_float("N/A")
    print ""

    print _yahoo_to_tmx_stock_name("CP.TO")
    print _yahoo_to_tmx_stock_name("AP-UN.TO")
    print _yahoo_to_tmx_stock_name("MMM")
    print ""

    print _get_url("https://www.google.ca")[0:200]
    print ""

    print _download_tmx_page('XBB.TO')[0:200]
    print ""

    for s in ["NA.TO", "XBB.TO", "BRK-A", "AAPL"]:
        print "============================================="
        print "s " + s

        print "get_company_name", get_company_name(s)
        print "price", get_price(s)
        print "get_52_week_low", get_52_week_low(s)
        print "get_52_week_high", get_52_week_high(s)
        print "get_volume", get_volume(s)
        print "get_change", get_change(s)
        print "get_stock_exchange", get_stock_exchange(s)

        #print "rp", relative_position(s)
        #print "rr", relative_range(s)
        #print "TI", test_indicator(s)

        #print get_currency("CP.TO")
        #d = get_all("CP.TO")
        #print d


if __name__ == '__main__':
    _main()

