# To make print working for Python2/3
from __future__ import print_function

# Is it worth to rebalance regularly a portfolio to keep the desired target allocation?
# Will the trading commissions eat up our profit?
# What if the commission was zero?

import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import finance_utils as fu
import stock_db_mgr as sdm
import virtual_account as va

start_date = datetime.date(2014, 1, 6)
end_date = datetime.date.today()
data_dir = './stock_db/qt'

db = sdm.StockDBMgr(data_dir, start_date, end_date, False)
# db.update_all_symbols()
dic = db.get_all_symbol_data()


def calc_commission_zero(nb_share):
    return 0


def simulate(rebalance_freq=1):
    initial_cash = 300000.0
    a = va.VirtualAccount(initial_cash, dic)

    #print("Initial cash", a.get_cash())

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
        if i % rebalance_freq == 0:
            #print("Rebalance", i)

            # Roughly Matching StockPortfolio_RRSP column ordering

            df['Price'] = df_prices.iloc[i]

            df['MktValue'] = df['Price'] * df['NbShare']

            total_value = df['MktValue'].sum() + a.get_cash()

            # Check if enough to cover for commission costs
            try_again = True
            while try_again:
                df['TgtValue'] = df['TgtAlloc'] * total_value

                # +:Buy -:Sell
                df['DeltaShare'] = np.floor(df['TgtValue'] / df['Price']) - df['NbShare']

                df['Commission'] = df['DeltaShare'].apply(fu.calc_commission_etf)
                # df['Commission'] = df['DeltaShare'].apply(calc_commission_zero)

                # Test run
                cash = a.get_cash()
                for s in df.index:
                    n = df.loc[s, 'DeltaShare']
                    if n < 0:
                        cash += (-n * df.loc[s, 'Price'] - df.loc[s, 'Commission'])
                    if n > 0:
                        cash += (-(n * df.loc[s, 'Price'] + df.loc[s, 'Commission']))
                if cash < 0:
                    total_commission = df['Commission'].sum()
                    # print("problem.................")
                    total_value -= total_commission
                else:
                    try_again = False

            # Sell first
            for s in df.index:
                n = df.loc[s, 'DeltaShare']
                if n < 0:
                    #print("  Sell {} of {}".format(-n, s))
                    a.delta_cash(-n * df.loc[s, 'Price'] - df.loc[s, 'Commission'])
                    df.loc[s, 'NbShare'] += n
                    #a.sell_at_market()

            # Buy second
            for s in df.index:
                n = df.loc[s, 'DeltaShare']
                if n > 0:
                    #print("  Buy {} of {}".format(n, s))
                    a.delta_cash(-(n * df.loc[s, 'Price'] + df.loc[s, 'Commission']))
                    df.loc[s, 'NbShare'] += n
                    #a.buy_at_market(i, s, n)

            # Do not tolerate negative cash after all transactions are completed.
            if a.get_cash() < 0:
                print("Error: not enough money", a.get_cash())

        else:
            #print("skip", i)
            pass

    # print("Initial Cash =", initial_cash)
    # Update last price
    df['Price'] = [dic[s].iloc[-1]['Close'] for s in symbol_list]
    final_cash = sum(df['Price'] * df['NbShare']) + a.get_cash()
    # print("Final Cash = ", final_cash)

    return (final_cash - initial_cash) / initial_cash


def _main():
    nb_days = len(db.get_symbol_data('XBB.TO'))
    freq_array = range(1, nb_days // 2)
    gain_array = []

    print("Running simulation for {} days...".format(nb_days))
    for relalance_freq in freq_array:
        gain = simulate(relalance_freq)
        gain_array += [gain]
        print("{}\t{}".format(relalance_freq, gain))

    plt.plot(freq_array, gain_array, 'o')
    plt.show()

if __name__ == '__main__':
    _main()

