"""yqd.py - Yahoo Quote Downloader.

Created on May 18 2017
@author: c0redumb

Starting on May 2017, Yahoo financial has terminated its service on
the well used EOD data download without warning. This is confirmed
by Yahoo employee in forum posts.

Yahoo financial EOD data, however, still works on Yahoo financial pages.
These download links uses a "crumb" for authentication with a cookie "B".
This code is provided to obtain such matching cookie and crumb.
"""

# To make print working for Python2/3
from __future__ import print_function

import time
import re

# Use six to import urllib so it is working for Python2/3
from six.moves import urllib

# Build the cookie handler
cookier = urllib.request.HTTPCookieProcessor()
opener = urllib.request.build_opener(cookier)
urllib.request.install_opener(opener)

# Cookie and corresponding crumb
_crumb = None

# Headers to fake a user agent
_headers = {
    'User-Agent':   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/41.0.2272.101 Safari/537.36'
}


def _get_cookie_crumb():
    """Performs a query and extract the matching cookie and crumb."""
    global _crumb

    # Perform a Yahoo financial lookup on SP500: ticker = ^GSPC
    cookier.cookiejar.clear()
    req = urllib.request.Request(
        'https://finance.yahoo.com/quote/%5EGSPC', headers=_headers)
    f = urllib.request.urlopen(req, timeout=5)
    alines = f.read().decode('utf-8')

    # Extract the crumb from the response
    # Looking for: "crumb":"xxxxxxxxxx"
    m = re.search('"crumb":"(.+?)"', alines)
    if m is not None:
        _crumb = m.group(1)

    if _crumb is None:
        raise AssertionError('Could not get initial cookie crumb from Yahoo.')


def load_yahoo_quote(ticker, begindate, enddate, info='quote'):
    """Loads the corresponding history/divident/split from Yahoo.

    The "begindate" and "enddate" are strings in the format of YYYYMMDD are are inclusive.
    The "info" can be "quote" for price, "dividend" for dividend events,
    or "split" for split events.

    The whole data is returned as a single string with newlines.
    """
    # Check to make sure that the cookie and crumb has been loaded
    if _crumb is None:
        _get_cookie_crumb()

    # Prepare the parameters and the URL
    tb = time.mktime((int(begindate[0:4]), int(
        begindate[4:6]), int(begindate[6:8]), 4, 0, 0, 0, 0, 0))
    te = time.mktime((int(enddate[0:4]), int(
        enddate[4:6]), int(enddate[6:8]), 18, 0, 0, 0, 0, 0))

    param = dict()
    param['period1'] = int(tb)
    param['period2'] = int(te)
    param['interval'] = '1d'
    if info == 'quote':
        param['events'] = 'history'
    elif info == 'dividend':
        param['events'] = 'div'
    elif info == 'split':
        param['events'] = 'split'
    param['crumb'] = _crumb
    params = urllib.parse.urlencode(param)
    url = 'https://query1.finance.yahoo.com/v7/finance/download/{}?{}'.format(
        urllib.parse.quote(ticker), params)
    # print(url)
    req = urllib.request.Request(url, headers=_headers)

    # Perform the query
    # There is no need to enter the cookie here, as it is automatically handled by opener
    alines = ""
    try_again = True
    try_count = 3
    while try_again and try_count > 0:
        try:
            f = urllib.request.urlopen(req, timeout=5)
            alines = f.read().decode('utf-8')
            try_again = False
        except Exception:
            try_count = try_count - 1
            # print("Error, will try again:", ticker)
            alines = ""

    if len(alines) < 5:
        print('\nERROR: Symbol not found:', ticker)

    return alines
