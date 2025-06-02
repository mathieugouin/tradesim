"""yqd.py - Yahoo Quote Downloader."""

import yfinance as yf


def load_yahoo_quote(ticker, begindate, enddate, filename):
    """Loads the corresponding history from Yahoo.

    The "begindate" and "enddate" are strings in the format of YYYYMMDD are are inclusive.

    The downloaded data is written to filename.
    """

    def to_iso_date(yyyymmdd):
        return yyyymmdd[0:4] + '-' + yyyymmdd[4:6] + '-' + yyyymmdd[6:]

    df = yf.download(
        tickers=ticker,
        start=to_iso_date(begindate), end=to_iso_date(enddate),
        group_by='ticker', multi_level_index=False,
        progress=False, auto_adjust=True, back_adjust=True)

    if len(df) > 0:
        df.to_csv(filename)
