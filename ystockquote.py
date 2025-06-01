"""Yahoo Stock Quote module provides a Python API for retrieving stock data from Yahoo."""

import yfinance as yf

_cached_ticker = {}


def _get_info(symbol, data):
    symbol = symbol.upper()
    ticker = None
    if symbol in _cached_ticker:
        ticker = _cached_ticker[symbol]
    else:
        ticker = yf.Ticker(symbol)
        _cached_ticker[symbol] = ticker

    info = ticker.info
    if data in info:
        value = ticker.info[data]
    else:
        value = None

    return value


def _get_info_choice(symbol, data_choice):
    value = None
    for data in data_choice:
        value = _get_info(symbol, data)
        if value is not None:
            break
    return value


def get_name(symbol):
    """Full company name from symbol."""
    return _get_info(symbol, 'longName')


def get_volume(symbol):
    """Current day's trading volume in number of shares."""
    return _get_info(symbol, 'volume')


def get_price(symbol):
    """Current day's trading last price."""
    #                                                                       For ETF??
    return _get_info_choice(symbol, ['regularMarketPrice', 'currentPrice', 'ask', 'navPrice'])


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
    return _get_info_choice(symbol, ['marketCap', 'totalAssets'])


def get_dividend_yield(symbol):
    """Return the dividend yield (in %) of the stock."""
    dividend = _get_info_choice(
            symbol,
            # TBD to confirm, ref tradesim_notebook.ipynb Yield Tests
            [
                'yield',
                'dividendYield',
                'trailingAnnualDividendYield',
            ]
        )
    if dividend is not None:
        # TBD not required?
        # dividend *= 100.0  # Bring to percentage
        pass
    else:
        dividend = 0.0
    return dividend


def get_price_earnings_ratio(symbol):
    """Return the P/E ratio."""
    return _get_info(symbol, 'trailingPE')
