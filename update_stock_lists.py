import pandas as pd


_headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9",
    "priority": "u=0, i",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
}


def update_dj():
    """Update Dow Jones list"""
    h = pd.read_html(
        "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average",
        keep_default_na=False,
        storage_options=_headers,
    )
    df = h[2]  # 3rd table

    # Make sure Symbol column is first, only keep relevant columns
    df = df.loc[:, ["Symbol", "Company"]]

    df = df.sort_values(by="Symbol")

    # yahoo use - instead of .
    df["Symbol"] = df["Symbol"].map(lambda s: s.replace(".", "-"))

    # insert comment
    df = df.rename(columns={"Symbol": "# Symbol"})

    # write
    df.to_csv("stock_db/dj.txt", sep="\t", index=False, encoding="utf-8")


def update_tsx():
    """Update TSX list"""
    h = pd.read_html(
        "https://en.wikipedia.org/wiki/S%26P/TSX_Composite_Index",
        keep_default_na=False,
        storage_options=_headers,
    )

    df = None
    found = False
    for df in h:
        if "Ticker" in df.columns and "Company" in df.columns:
            found = True
            break

    if not found:
        return

    df = df.rename(columns={"Ticker": "Symbol"})

    # Make sure Symbol column is first, only keep relevant columns
    df = df.loc[:, ["Symbol", "Company"]]

    df = df.sort_values(by="Symbol")

    # yahoo use - instead of .
    df["Symbol"] = df["Symbol"].map(lambda s: s.replace(".", "-"))

    # .TO for yahoo
    df["Symbol"] = df["Symbol"].map(lambda s: s + ".TO")

    # insert comment
    df = df.rename(columns={"Symbol": "# Symbol"})

    # write
    df.to_csv("stock_db/tsx.txt", sep="\t", index=False, encoding="utf-8")


def update_sp500():
    """Update SP-500 list"""
    h = pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
        keep_default_na=False,
        storage_options=_headers,
    )
    df = h[0]  # first table

    # Make sure Symbol column is first, only keep relevant columns
    df = df.loc[:, ["Symbol", "Security"]]

    df = df.rename(columns={"Security": "Company"})

    df = df.sort_values(by="Symbol")

    # yahoo use - instead of .
    df["Symbol"] = df["Symbol"].map(lambda s: s.replace(".", "-"))

    # insert comment
    df = df.rename(columns={"Symbol": "# Symbol"})

    # write
    df.to_csv("stock_db/sp500.txt", sep="\t", index=False, encoding="utf-8")


def _main():
    update_dj()
    update_tsx()  # TBD wiki not fully up-to-date
    update_sp500()


if __name__ == "__main__":
    _main()
