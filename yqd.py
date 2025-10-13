"""yqd.py - Yahoo Quote Downloader."""

import yfinance as yf
import traceback


def load_yahoo_quote(ticker, begindate, enddate, filename):
    """Load the corresponding history from Yahoo.

    The "begindate" and "enddate" are strings in the format of YYYYMMDD
    and are are inclusive.

    The downloaded data is written to filename.
    """

    def to_iso_date(yyyymmdd):
        return yyyymmdd[0:4] + "-" + yyyymmdd[4:6] + "-" + yyyymmdd[6:]

    try:
        df = yf.download(
            tickers=ticker,
            start=to_iso_date(begindate), end=to_iso_date(enddate),
            group_by="ticker", multi_level_index=False,
            progress=False, auto_adjust=True, back_adjust=True)

        if len(df) > 0:
            df.to_csv(filename)
    except Exception as e:
        print(f"Error: failed to download {ticker}. {e}")
        traceback.print_exc()
