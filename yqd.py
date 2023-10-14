"""yqd.py - Yahoo Quote Downloader.

Created on May 18 2017
@author: c0redumb

Starting on May 2017, Yahoo financial has terminated its service on
the well used EOD data download without warning. This is confirmed
by Yahoo employee in forum posts.

Yahoo financial EOD data, however, still works on Yahoo financial pages.
These download links uses a "crumb" for authentication with a cookie "B".
This code is provided to obtain such matching cookie and crumb.

Updates: Mathieu Gouin
"""

# To make print working for Python2/3
from __future__ import print_function

import time
import requests

# Cookie and corresponding crumb
_crumb = None

# Headers to fake a user agent
_HEADERS = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

def _get_cookie_crumb():
    """Performs a query and extract the matching cookie and crumb."""
    global _crumb

    crumb = None

    # You can tell Requests to stop waiting for a response after
    # a given number of seconds with the timeout parameter.
    # Nearly all production code should use this parameter in nearly all requests.
    try:
        response = requests.get(
            "https://fc.yahoo.com",
            headers=_HEADERS,
            allow_redirects=True,
            timeout=1
        )
        if not response.cookies:
            raise AssertionError("Failed to obtain Yahoo auth cookie.")

        cookie = list(response.cookies)[0]
        crumb_response = requests.get(
            "https://query1.finance.yahoo.com/v1/test/getcrumb",
            headers=_HEADERS,
            cookies={cookie.name: cookie.value},
            allow_redirects=True,
            timeout=1
        )
        crumb = crumb_response.text
    except Exception as exc:
        raise AssertionError('Could not get initial cookie crumb from Yahoo. ' + str(exc))

    if crumb is None or len(crumb) < 3:
        raise AssertionError('Could not get initial cookie crumb from Yahoo.')

    # Store it globally
    _crumb = crumb


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
    time_begin = time.mktime((int(begindate[0:4]), int(
        begindate[4:6]), int(begindate[6:8]), 4, 0, 0, 0, 0, 0))
    time_end = time.mktime((int(enddate[0:4]), int(
        enddate[4:6]), int(enddate[6:8]), 18, 0, 0, 0, 0, 0))

    params = {}
    params['period1'] = int(time_begin)
    params['period2'] = int(time_end)
    params['interval'] = '1d'
    if info == 'quote':
        params['events'] = 'history'
    elif info == 'dividend':
        params['events'] = 'div'
    elif info == 'split':
        params['events'] = 'split'
    params['crumb'] = _crumb

    alines = ""
    try:
        response = requests.get(
            "https://query1.finance.yahoo.com/v7/finance/download/" + ticker,
            headers=_HEADERS,
            allow_redirects=True,
            params=params,
            timeout=1
        )
        alines = response.text
    except Exception:
        alines = ""

    if len(alines) < len("Date,Open,High,Low,Close,Adj Close,Volume"):
        print('\nERROR: Symbol not found:', ticker)
        alines = ""

    return alines
