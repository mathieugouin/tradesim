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
import requests

# Use six to import urllib so it is working for Python2/3
#from six.moves import urllib

# Cookie and corresponding crumb
_crumb = None

# Headers to fake a user agent
_headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

def get_yahoo_cookie():
    cookie = None

    # You can tell Requests to stop waiting for a response after a given number of seconds with the timeout parameter. Nearly all production code should use this parameter in nearly all requests.
    response = requests.get(
        "https://fc.yahoo.com",
        headers=_headers,
        allow_redirects=True,
        timeout=1
    )

    if not response.cookies:
        raise AssertionError("Failed to obtain Yahoo auth cookie.")

    cookie = list(response.cookies)[0]

    return cookie


def get_yahoo_crumb(cookie):
    crumb = None

    crumb_response = requests.get(
        "https://query1.finance.yahoo.com/v1/test/getcrumb",
        headers=_headers,
        cookies={cookie.name: cookie.value},
        allow_redirects=True,
        timeout=1
    )
    crumb = crumb_response.text

    if crumb is None:
        raise AssertionError('Could not get initial cookie crumb from Yahoo.')

    return crumb


def _get_cookie_crumb():
    """Performs a query and extract the matching cookie and crumb."""
    global _crumb

    # Usage
    cookie = get_yahoo_cookie()
    crumb = get_yahoo_crumb(cookie)
    _crumb = crumb
    return


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

    param = {}
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

    alines = ""
    try:
        response = requests.get(
            "https://query1.finance.yahoo.com/v7/finance/download/" + ticker,
            headers=_headers,
            allow_redirects=True,
            data=param,
            timeout=1
        )
        alines = response.text
    except Exception as exc:
        alines = ""
        print(type(exc))  # the exception instance
        print(exc.args)  # arguments stored in .args
        print(exc)  # __str__ allows args to be printed directly

    if len(alines) < 5:
        print('\nERROR: Symbol not found:', ticker)

    return alines
