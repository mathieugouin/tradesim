# To make print working for Python2/3
from __future__ import print_function

import position
import math


def calcCommission(nbShare):
    """Commission cost based on nb of shares.  Valid for Questrade stock trading only."""
    return nbShare * 0.0035 + min(9.95, max(0.01 * nbShare, 4.95))


class VirtualAccount(object):

    """Handles an account linked to a stock DB."""

    def __init__(self, initialCapital, dataDic):
        """Instantiate a new virtual account object."""
        self._initialCapital = initialCapital
        self._cash = self._initialCapital
        self._dataDic = dataDic
        self._positions = []

    def buyAtMarket(self, bar, symbol, nbShare, name="buyAtMarket"):
        print("buyAtMarket()")
        nbShare = math.floor(nbShare)
        if nbShare > 0:
            #buyPrice = dataDic[symbol].iloc[bar]['Close']
            buyPrice = self._dataDic[symbol].iloc[bar]['High'] # Worst case simulation
            commission = calcCommission(nbShare)
            cost = buyPrice * nbShare + commission
            if cost < self._cash:
                self._positions.append(position.Position(bar, symbol, nbShare, buyPrice, name, commission))
                self._cash -= cost
            else:
                print("Error: not enough money")
        else:
            print("Error: can't buy 0 share")

    def sellAtMarket(self, position, bar, name="sellAtMarket"):
        print("sellAtMarket()")
        # sellPrice = dataDic[position.getSymbol()].iloc[bar]['Close']
        sellPrice = self._dataDic[position.getSymbol()].iloc[bar]['Low'] # Worst case
        cost = calcCommission(position.getNbShare())
        if cost < self._cash:
            self._cash -= cost
            self._cash += position.close(bar, sellPrice, name)
        else:
            print("Error: not enough money")

    def getAllPositions(self, symbol=""):
        if symbol in self._dataDic.keys():
            return [p for p in self._positions if p.getSymbol() == symbol] # positions only for symbol
        else:
            return self._positions # all positions

    def getOpenPositions(self, symbol=""):
        if symbol in self._dataDic.keys():
            return [p for p in self._positions if p.getSymbol() == symbol and p.isOpen()] # open positions only for symbol
        else:
            return [p for p in self._positions if p.isOpen()] # all open positions

    def getClosePositions(self, symbol=""):
        if symbol in self._dataDic.keys():
            return [p for p in self._positions if p.getSymbol() == symbol and not p.isOpen()] # close positions only for symbol
        else:
            return [p for p in self._positions if not p.isOpen()] # all close positions

    def getCash(self):
        return self._cash

    def deltaCash(self, delta):
        self._cash += delta
        if self._cash < 0:
            #print("Error: not enough money: {}".format(wouldBeCash))
            pass


def __print_position(va):
    print("all pos = {}".format([str(p) for p in va.getAllPositions()]))
    print("open pos = {}".format([str(p) for p in va.getOpenPositions()]))
    print("closed pos = {}".format([str(p) for p in va.getClosePositions()]))


def __main():
    import stock_db_mgr as sdm
    db = sdm.StockDBMgr('./stock_db/qt')
    va = VirtualAccount(100000, db.getAllSymbolDataDic())
    print("comm = {}".format(calcCommission(300)))
    print("$ = {}".format(va.getCash()))
    va.deltaCash(100)
    print("$ = {}".format(va.getCash()))
    va.deltaCash(-200)
    print("$ = {}".format(va.getCash()))
    __print_position(va)
    va.buyAtMarket(3, 'XBB.TO', 100)
    __print_position(va)
    va.buyAtMarket(6, 'XEC.TO', 200)
    __print_position(va)
    va.sellAtMarket(va.getAllPositions()[0], 12)
    __print_position(va)


if __name__ == '__main__':
    __main()
