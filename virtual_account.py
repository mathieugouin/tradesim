# To make print working for Python2/3
from __future__ import print_function

import position
import math
import finance_utils as fu


class VirtualAccount(object):
    """Handles an account linked to a stock DB.

    Does not support partial sell of position."""

    def __init__(self, initial_capital, data_dic):
        """Instantiate a new virtual account object."""
        self._cash = initial_capital
        self._data_dic = data_dic
        self._positions = []

    def buy_at_market(self, bar, symbol, nb_share, name="buy_at_market"):
        print("buy_at_market()")
        nb_share = math.floor(nb_share)
        if nb_share > 0:
            buy_price = self._data_dic[symbol].iloc[bar]['High']  # Worst case simulation
            commission = fu.calc_commission(nb_share)
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
        if position.is_open():
            sell_price = self._data_dic[position.get_symbol()].iloc[bar]['Low'] # Worst case
            cost = fu.calc_commission(position.get_nb_share())
            if cost < self._cash:
                self._cash -= cost
                self._cash += position.close(bar, sell_price, name)
            else:
                print("Error: not enough money")
        else:
            print("Error: position already closed")

    def get_all_positions(self, symbol=""):
        if symbol in self._data_dic:
            # positions only for symbol
            return [p for p in self._positions if p.get_symbol() == symbol]
        # all positions
        return self._positions

    def get_open_positions(self, symbol=""):
        if symbol in self._data_dic:
            # open positions only for symbol
            return [p for p in self._positions if p.get_symbol() == symbol and p.is_open()]
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
            print("Error: not enough money: {}".format(self._cash))
            pass
