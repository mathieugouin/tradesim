"""Yahoo Stock Quote module provides a Python API for retrieving stock data from Yahoo."""

import yfinance as yf

_cached_ticker = {}


def _get_info(symbol, data):
    symbol = symbol.upper()
    t = None
    if symbol in _cached_ticker:
        t = _cached_ticker[symbol]
    else:
        t = yf.Ticker(symbol)
        _cached_ticker[symbol] = t

    i = t.info
    if data in i:
        v = t.info[data]
    else:
        v = None

    return v


def get_name(symbol):
    """Full company name from symbol."""
    return _get_info(symbol, 'longName')


def get_volume(symbol):
    """Current day's trading volume in number of shares."""
    return _get_info(symbol, 'volume')


def get_price(symbol):
    """Current day's trading last price."""
    # TBD to confirm
    return _get_info(symbol, 'regularMarketPrice')
    #return _get_info(symbol, 'currentPrice')


def get_stock_exchange(symbol):
    """Return the name of the stock exchange the stock is traded."""
    return _get_info(symbol, 'exchange')


def get_52_week_high(symbol):
    """Highest price value during the last 52 weeks."""
    return _get_info(symbol, 'fiftyTwoWeekHigh')


def get_52_week_low(symbol):
    """Lowest price value during the last 52 weeks."""
    return _get_info(symbol, 'fiftyTwoWeekLow')


def get_currency(symbol):
    return _get_info(symbol, 'currency')


def get_market_cap(symbol):
    """Return the market capitalization of the given stock."""
    m = _get_info(symbol, 'marketCap')
    if m is None:
        m = _get_info(symbol, 'totalAssets')
    return m

def get_dividend_yield(symbol):
    """Return the dividend yield (in %) of the stock."""
    return 100 * _get_info(symbol, 'trailingAnnualDividendYield')


def get_price_earnings_ratio(symbol):
    """Return the P/E ratio."""
    return _get_info(symbol, 'trailingPE')
