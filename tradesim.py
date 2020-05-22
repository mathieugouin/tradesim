# NOTES:
# http://stats.stackexchange.com/questions/1595/python-as-a-statistics-workbench
# http://en.wikipedia.org/wiki/Algorithmic_trading

# To make print working for Python2/3
from __future__ import print_function

import math
import datetime

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import finance_utils as fu
import technical_indicators as ti
import stock_db_mgr as sdm
import virtual_account as va

# start_date = datetime.date(1900, 1, 1)
start_date = datetime.date(2014, 1, 1)

# end_date = datetime.date(2018, 12, 31)
end_date = datetime.date.today()

# default
data_dir = './stock_db/test'
# Global stock dictionary
dic = {}
db = None


def simulate():
    print("simulate()")

    a = va.VirtualAccount(50000.00, dic)

    print("Initial cash", a.get_cash())

    # Symbol loop
    symbol_list = list(dic.keys())
    symbol_list.sort()
    for symbol in symbol_list:
        print("Simulating with", symbol)
        df = dic[symbol]

        # The various series (starting with s):
        s_close = fu.get_close(df)

        # Technical indicators
        s_close_sma = ti.sma(s_close, 200)

        # Bar loops (1 bar per day)
        # start index to include various moving average lag
        # end at -1 to include "tomorrow" (corresponds to last valid bar)
        # TBD to fix this with real signals
        for bar in range(200, len(df) - 1):
            # Positions loop
            open_positions = a.get_open_positions(symbol)
            for pos in open_positions:
                # TBD sell logic
                sell_signal = s_close[bar] > 1.15 * pos.get_entry_price() or \
                              s_close[bar] < 0.95 * pos.get_entry_price()
                if sell_signal:
                    a.sell_at_market(pos, bar + 1)  # bar + 1 = tomorrow
            if not open_positions:
                # TBD buy logic
                buy_signal = ti.cross_over(s_close, s_close_sma)[bar]
                if buy_signal:
                    nb_share = int(2500 / s_close[bar])  # 2500$ => about 0.8% commission buy + sell
                    a.buy_at_market(bar + 1, symbol, nb_share) # bar + 1 = tomorrow

    for p in a.get_all_positions():
        print(p)

    print("Final cash", a.get_cash())


def plot_test():
    print("plot_test()")

    symbol_list = list(dic.keys())
    symbol_list.sort()
    for symbol in symbol_list:
        print("Plotting with " + symbol)
        df = dic[symbol]

        x = fu.get_close(df)
        t = np.arange(len(x))
        plt.plot(t, x,)
        # plt.plot(t, ti.sma(x, 200))
        # plt.plot(t, ti.ema(x, 200))
        # plt.plot(t, ti.linear_fit(x, 200))
        plt.plot(t, ti.iir_lowpass(x, 3, 200))
        # plt.plot(t, ti.aema(x, 200))
        plt.grid(True)
        plt.title(symbol)
        plt.show()


def load_data():
    print("load_data()")

    global dic
    global db

    db = sdm.StockDBMgr(data_dir, start_date, end_date)

    dic = db.get_all_symbol_data()


def _main():
    print("main()")

    load_data()

    plot_test()

    simulate()


if __name__ == '__main__':
    _main()
