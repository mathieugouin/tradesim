# To make print working for Python2/3
from __future__ import print_function

import position
import math


def calc_commission(nb_share):
    """Commission cost based on nb of shares.  Valid for Questrade stock trading only."""
    return nb_share * 0.0035 + min(9.95, max(0.01 * nb_share, 4.95))


class VirtualAccount(object):
    """Handles an account linked to a stock DB."""

    def __init__(self, initial_capital, data_dic):
        """Instantiate a new virtual account object."""
        self._cash = initial_capital
        self._data_dic = data_dic
        self._positions = []

    def buy_at_market(self, bar, symbol, nb_share, name="buy_at_market"):
        print("buy_at_market()")
        nb_share = math.floor(nb_share)
        if nb_share > 0:
            buy_price = self._data_dic[symbol].iloc[bar]['High'] # Worst case simulation
            commission = calc_commission(nb_share)
            cost = buy_price * nb_share + commission
            if cost < self._cash:
                self._positions.append(position.Position(bar, symbol, nb_share, buy_price, name, commission))
                self._cash -= cost
            else:
                print("Error: not enough money")
        else:
            print("Error: can't buy 0 share")

    def sell_at_market(self, position, bar, name="sell_at_market"):
        print("sell_at_market()")
        sell_price = self._data_dic[position.get_symbol()].iloc[bar]['Low'] # Worst case
        cost = calc_commission(position.get_nb_share())
        if cost < self._cash:
            self._cash -= cost
            self._cash += position.close(bar, sell_price, name)
        else:
            print("Error: not enough money")

    def get_all_positions(self, symbol=""):
        if symbol in self._data_dic:
            # positions only for symbol
            return [p for p in self._positions if p.get_symbol() == symbol]
        else:
            # all positions
            return self._positions

    def get_open_positions(self, symbol=""):
        if symbol in self._data_dic:
            # open positions only for symbol
            return [p for p in self._positions if p.get_symbol() == symbol and p.is_open()]
        else:
            # all open positions
            return [p for p in self._positions if p.is_open()]

    def get_close_positions(self, symbol=""):
        if symbol in self._data_dic:
            # close positions only for symbol
            return [p for p in self._positions if p.get_symbol() == symbol and not p.is_open()]
        # all close positions
        return [p for p in self._positions if not p.is_open()]

    def get_cash(self):
        return self._cash

    def delta_cash(self, delta):
        self._cash += delta
        if self._cash < 0:
            #print("Error: not enough money: {}".format(wouldBeCash))
            pass


def __print_position(va):
    print("all pos = {}".format([str(p) for p in va.get_all_positions()]))
    print("open pos = {}".format([str(p) for p in va.get_open_positions()]))
    print("closed pos = {}".format([str(p) for p in va.get_close_positions()]))

    print("all pos (XBB.TO) = {}".format([str(p) for p in va.get_all_positions('XBB.TO')]))
    print("open pos (XBB.TO) = {}".format([str(p) for p in va.get_open_positions('XBB.TO')]))
    print("closed pos (XBB.TO) = {}".format([str(p) for p in va.get_close_positions('XBB.TO')]))


def __main():
    import stock_db_mgr as sdm
    db = sdm.StockDBMgr('./stock_db/qt')
    va = VirtualAccount(100000, db.getAllSymbolDataDic())
    print("comm = {}".format(calc_commission(300)))
    print("$ = {}".format(va.get_cash()))
    va.delta_cash(100)
    print("$ = {}".format(va.get_cash()))
    va.delta_cash(-200)
    print("$ = {}".format(va.get_cash()))
    __print_position(va)
    va.buy_at_market(3, 'XBB.TO', 100)
    __print_position(va)
    va.buy_at_market(6, 'XEC.TO', 200)
    __print_position(va)
    va.sell_at_market(va.get_all_positions()[0], 12)
    __print_position(va)


if __name__ == '__main__':
    __main()
