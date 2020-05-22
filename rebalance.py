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

start_date = datetime.date(2014, 1, 6)
end_date = datetime.date.today()
data_dir = './stock_db/qt'


# TBD move out to finance utils
def calc_commission_etf(nbShare):
    """Return the ETF trade commission: positive=Buy, negative=Sell."""
    return (nbShare < 0) * min(9.95, max(4.95, -nbShare * 0.01)) + math.fabs(nbShare) * 0.0035


def simulate():
    db = sdm.StockDBMgr(data_dir, start_date, end_date, False)

    dic = db.get_all_symbol_data()

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

    assert sum(ratio.values()) == 1.0

    symbol_list = list(dic.keys())
    symbol_list.sort()

    df = pd.DataFrame(
        index=symbol_list,
        data=[ratio[s] for s in symbol_list],
        columns=['TgtAlloc'])

    df['NbShare'] = np.zeros(len(symbol_list))

    df_prices = db.get_all_symbol_single_data_item('Close')
    for i in range(len(df_prices)):
        if i % 10 == 0:  # Adjust rebalance frequency here
            print("Rebalance", i)

            # Roughly Matching StockPortfolio_RRSP column ordering

            df['Price'] = df_prices.iloc[i]

            df['MktValue'] = df['Price'] * df['NbShare']

            total_value = df['MktValue'].sum() + a.get_cash()

            df['CurrAlloc'] = df['MktValue'] / total_value
            df['DeltaAlloc'] = df['CurrAlloc'] - df['TgtAlloc']  # Not required

            df['TgtValue'] = df['TgtAlloc'] * total_value

            # +:Buy  -:Sell
            df['DeltaShare'] = np.floor(df['TgtValue'] / df['Price']) - df['NbShare']

            # c = [calc_commission_etf(n) for n in df['DeltaShare'].values]
            df['Commission'] = df['DeltaShare'].apply(calc_commission_etf)

            # TBD not sure about the commission formula for both buy & sell...
            # TBD Probably need to sell first, then buy

            for s in df.index:
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


def _main():
    simulate()

if __name__ == '__main__':
    _main()
