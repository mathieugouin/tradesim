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

# Start of Questrade portfolio
start_date = datetime.date(2014, 1, 6)

# Start of Questrade portfolio component highest start date (VUN.TO)
# start_date = datetime.date(2013, 8, 12)

end_date = datetime.date.today()

# default
data_dir = './stock_db/qt'
# Global stock dictionary
dic = {}
db = None


def calc_commission_etf(nbShare):
    """Return the ETF trade commission: positive=Buy, negative=Sell."""
    return (nbShare < 0) * min(9.95, max(4.95, -nbShare * 0.01)) + math.fabs(nbShare) * 0.0035


def simulate():
    print("simulate()")

    initial_cash = 100000.0
    a = va.VirtualAccount(initial_cash, dic)

    print("Initial cash", a.get_cash())

    # Target allocation:
    ratio = {
        'XBB.TO': 0.1,
        'ZCN.TO': 0.3,
        'VUN.TO': 0.3,
        'XEF.TO': 0.2,
        'XEC.TO': 0.1
    }

    # Symbol loop
    symbol_list = list(dic.keys())
    symbol_list.sort()

    df = pd.DataFrame(
        index=symbol_list,
        data=[ratio[s] for s in symbol_list],
        columns=['TgtAlloc'])

    df['NbShare'] = np.zeros(len(symbol_list))

    df_prices = db.get_all_symbol_single_data_item('Close')
    for i in range(len(df_prices)):
        if i % 100 == 0:  # Adjust rebalance frequency here
            print("Rebalance", i)

            # Roughly Matching StockPortfolio_RRSP column ordering

            df['Price'] = df_prices.iloc[i]

            df['MktValue'] = df['Price'] * df['NbShare']

            total_value = sum(df['Price'] * df['NbShare']) + a.get_cash()

            df['CurrAlloc'] = df['MktValue'] / total_value
            df['DeltaAlloc'] = df['CurrAlloc'] - df['TgtAlloc']

            df['TgtValue'] = df['TgtAlloc'] * total_value

            # +:Buy  -:Sell
            df['DeltaShare'] = np.floor((df['TgtValue']) / df['Price']) - df['NbShare']

            c = [calc_commission_etf(n) for n in df['DeltaShare'].values]

            # TBD not sure about the commission formula for both buy & sell...

            for s in symbol_list:
                n = df.loc[s, 'DeltaShare']
                if n > 0:
                    print("  Buy {} of {}".format(n, s))
                    a.delta_cash(-n * df.loc[s, 'Price'])
                    df.loc[s, 'NbShare'] += n
                    #a.buy_at_market(i, s, n)
                elif n < 0:
                    print("  Sell {} of {}".format(-n, s))
                    a.delta_cash(-n * df.loc[s, 'Price'])
                    df.loc[s, 'NbShare'] += n
                    #a.sell_at_market()

            # Do not tolerate after all transactions are done.
            if a.get_cash() < 0:
                print("Error: not enough money", a.get_cash())

        else:
            #print("skip", i)
            pass

    print("Initial Cash =", initial_cash)
    # Update last price
    df['Price'] = [dic[s].iloc[-1]['Close'] for s in symbol_list]
    print("Final Cash = ", sum(df['Price'] * df['NbShare']) + a.get_cash())


def simulate2():
    print("simulate2()")

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
    simulate2()


if __name__ == '__main__':
    _main()
