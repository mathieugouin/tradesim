"""Playground: various ideas testing code."""

# TBD: Could put all this in notebook.


import datetime
import pandas as pd

# user
import stock_db_mgr as sdm
import finance_utils as fu


startdate = datetime.date(2014, 1, 6)  # Start of Questrade portfolio
# startdate = datetime.date(2013, 8, 12)  # Start of Questrade portfolio component highest start date (VUN.TO)
today = datetime.date.today()

# Pick one:
# enddate = datetime.date(2018, 1, 1)
enddate = today


def indicator_test():
    print('indicator_test')

    db = sdm.StockDBMgr('stock_db/test', startdate, enddate)
    df = db.get_all_symbol_single_data_item('Close')
    print(df.describe())

    rp = (df.iloc[-1] - df.min()) / (df.max() - df.min())
    rps = 2.0 * rp - 1.0
    rr = (df.max() - df.min()) / df.max()

    t = rps * rr.pow(0.1)

    # Price in the floor (5% tolerance) & 15% drop
    print(t.loc[(rp < 0.05) & (rr > 0.15)])


def correlation_test():
    print('correlation_test')

    db = sdm.StockDBMgr('stock_db/test', startdate, enddate)
    df = db.get_all_symbol_single_data_item('Close')
    df = fu.clean_dataframe(df, startdate)
    df = fu.fill_nan_data(df)

    dfc = df.corr()

    with pd.option_context(
        "display.max_rows", None,
        "display.max_columns", None,
        "display.width", None,
        "display.max_colwidth", None
    ):
        print("Correlation matrix:")
        print(dfc)

        # Results
        dfr = pd.DataFrame(dfc.min(), columns=["Correlation"])
        dfr["Symbol"] = dfc.idxmin()
        dfr = dfr.sort_values(by=["Correlation"])
        print("Min correlation per symbol:")
        print(dfr)


def _main():
    indicator_test()
    correlation_test()


if __name__ == '__main__':
    _main()
