"""
yqd.py - Yahoo Quote Downloader.
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

# Use six to import urllib so it is working for Python2/3
from six.moves import urllib
# If you don't want to use six, please comment out the line above
# and use the line below instead (for Python3 only).
#import urllib.request, urllib.parse, urllib.error

import time

# Build the cookie handler
cookier = urllib.request.HTTPCookieProcessor()
opener = urllib.request.build_opener(cookier)
urllib.request.install_opener(opener)

# Cookie and corresponding crumb
_cookie = None
_crumb = None

# Headers to fake a user agent
_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
}


def _get_cookie_crumb():
    '''
    This function perform a query and extract the matching cookie and crumb.
    '''
    global cookier, _cookie, _crumb

    # Perform a Yahoo financial lookup on SP500
    cookier.cookiejar.clear()
    req = urllib.request.Request(
        'https://finance.yahoo.com/quote/^GSPC', headers=_headers)
    f = urllib.request.urlopen(req, timeout=5)
    alines = f.read().decode('utf-8')

    # Extract the crumb from the response
    cs = alines.find('CrumbStore')
    cr = alines.find('crumb', cs + 10)
    cl = alines.find(':', cr + 5)
    q1 = alines.find('"', cl + 1)
    q2 = alines.find('"', q1 + 1)
    crumb = alines[q1 + 1:q2]
    _crumb = crumb

    # Extract the cookie from cookiejar
    for c in cookier.cookiejar:
        if c.domain != '.yahoo.com':
            continue
        if c.name != 'B':
            continue
        _cookie = c.value

    # Print the cookie and crumb
    #print('Cookie:', _cookie)
    #print('Crumb:', _crumb)


# begindate & enddate are inclusive
# begindate, enddate format: YYYYMMDD
def load_yahoo_quote(ticker, begindate, enddate, info='quote'):
    """
    Loads the corresponding history/divident/split from Yahoo.
    The "begindate" and "enddate" are in the format of YYYYMMDD.
    The "info" can be "quote" for price, "divident" for divident events,
    or "split" for split events.
    """
    # Check to make sure that the cookie and crumb has been loaded
    global _cookie, _crumb
    if _cookie is None or _crumb is None:
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
        ticker, params)
    # print(url)
    req = urllib.request.Request(url, headers=_headers)

    # Perform the query
    # There is no need to enter the cookie here, as it is automatically handled by opener
    alines = ""
    tryAgain = True
    tryCount = 3
    while tryAgain and tryCount > 0:
        try:
            f = urllib.request.urlopen(req, timeout=5)
            alines = f.read().decode('utf-8')
            tryAgain = False
        except Exception:
            tryCount = tryCount - 1
            #print("Error, will try again:", ticker)
            alines = ""

    if len(alines) < 5:
        print('\nERROR: Symbol not found:', ticker)

    # print(alines)

    # return alines.split('\n')
    return alines


def _main():
    print("main")

    ticker = 'IBM'
    print('===', ticker, '===')
    lines = load_yahoo_quote(ticker, '20180212', '20180212').split('\n')
    for l in lines:
        print(l)

    ticker = 'ZCN.TO'
    print('===', ticker, '===')
    lines = load_yahoo_quote(ticker, '20180212', '20180213').split('\n')
    for l in lines:
        print(l)


if __name__ == "__main__":
    _main()

