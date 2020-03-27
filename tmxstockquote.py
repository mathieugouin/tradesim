#!/usr/bin/env python

# TBD not completed....

import urllib
import re
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
            # TBD Sleep?
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
    value = ""
    lines = _download_tmx_page(symbol)
    j = 0  # re_arr indexer
    if len(re_arr) > 0:
        for line in lines:
            m = re.search(re_arr[j], line)
            if m:
                # If we are at the last re
                if j == len(re_arr) - 1:
                    value = m.group(1)
                    break
                else:
                    j = j + 1  # continue at next re

    #myAssert_(value != "");

    return value


def _request_tmx_str(symbol, stat):
    re_str = re.escape(r'<td> <span class="l">') + \
             re.escape(stat) + \
             re.escape(r'</span></td><td> <span class="dt">') + '(.*?)' + \
             re.escape(r'</span></td>')

    return _request_tmx_re(symbol, re_str)


def _request_tmx(symbol, stat):
    return _str_to_float(_request_tmx_str(symbol, stat))


def get_price(symbol):
    # <div class="l-p c-d">$204.66</div>
    reStr = r'<div class="l-p (?:c-u)?(?:c-d)?">\$' + '([0-9\., ]+)'
    return _str_to_float(_request_tmx_re(symbol, reStr))


def get_company_name(symbol):
    re_str = re.escape('<h4>') + '(.*?)' + re.escape('</h4>')
    return _request_tmx_re(symbol, re_str)


def get_currency(symbol):
    return ""


def get_change(symbol):
    #   // US:    <div class="q-c"> <span class="c-u"> 1,581.01
    #   // CAN:   <td class="last">27.06</td><td class="c-d">-0.30 (-1.10%)</td></tr>
    reStr = r'(?:<div class="q-c"> <span class="(?:c-[ud])?">\s*|<td class="last">[0-9 ,.]+<\/td><td class="(?:c-[ud])?">)(-?[0-9 ,.]+)'
    return _str_to_float(_request_tmx_re(symbol, reStr))


def get_52_week_high(symbol):
    return _request_tmx(symbol, "Yr High:")


def get_52_week_low(symbol):
    return _request_tmx(symbol, "Yr Low:")


def get_stock_exchange(symbol):
    return _request_tmx_re(symbol, r'<div class="qmCompanyExchange">Exchange: (.+?)</div>')


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

        #print "price", get_price(s)
        #print "get_52_week_low", get_52_week_low(s)
        #print "get_52_week_high", get_52_week_high(s)
        print "get_company_name", get_company_name(s)
        #print "get_change", get_change(s)
        #print "get_stock_exchange", get_stock_exchange(s)

        #print "rp", relative_position(s)
        #print "rr", relative_range(s)
        #print "TI", test_indicator(s)

        #print get_currency("CP.TO")
        #d = get_all("CP.TO")
        #print d


if __name__ == '__main__':
    _main()

