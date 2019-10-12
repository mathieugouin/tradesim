import Position
import math

class CVirtualAccount:
    def __init__(self, initialCapital, dataDic):
        self._initialCapital    = initialCapital
        self._cash              = self._initialCapital
        self._dataDic           = dataDic
        self._positions         = []

    def calcComission(self, nbShare):
        return nbShare * 0.0045 + min(9.95, max(0.01 * nbShare, 4.95))

    def buyAtMarket(self, bar, symbol, nbShare, name = "buyAtMarket"):
        print "buyAtMarket()"
        nbShare = math.floor(nbShare)
        if nbShare > 0:
            #buyPrice = dataDic[symbol].iloc[bar]['Close']
            buyPrice = self._dataDic[symbol].iloc[bar]['High'] # Worst case simulation
            comission = self.calcComission(nbShare)
            cost = buyPrice * nbShare + comission;
            if cost < self._cash:
                self._positions.append(Position.CPosition(bar, symbol, nbShare, buyPrice, name, comission))
                self._cash -= cost
            else:
                print "Error: not enough money"
        else:
            print "Error: can't buy 0 share"

    def sellAtMarket(self, position, bar, name = "sellAtMarket"):
        print "sellAtMarket()"
        # sellPrice = dataDic[position.getSymbol()].iloc[bar]['Close']
        sellPrice = self._dataDic[position.getSymbol()].iloc[bar]['Low'] # Worst case
        cost = self.calcComission(position.getNbShare());
        if cost < self._cash:
            self._cash -= cost
            self._cash += position.close(bar, sellPrice, name)
        else:
            print "Error: not enough money"

    def getAllPositions(self, symbol = ""):
        if symbol in self._dataDic.keys():
            return [p for p in self._positions if p.getSymbol() == symbol] # positions only for symbol
        else:
            return self._positions # all positions

    def getOpenPositions(self, symbol = ""):
        if symbol in self._dataDic.keys():
            return [p for p in self._positions if p.getSymbol() == symbol and p.isOpen()] # open positions only for symbol
        else:
            return [p for p in self._positions if p.isOpen()] # all open positions

    def getClosePositions(self, symbol = ""):
        if symbol in self._dataDic.keys():
            return [p for p in self._positions if p.getSymbol() == symbol and not p.isOpen()] # close positions only for symbol
        else:
            return [p for p in self._positions if not p.isOpen()] # all close positions

    def getCash(self):
        return self._cash


def _main():
    import stock_db_mgr as sdm
    db = sdm.CStockDBMgr('./stock_db/qt')
    va = CVirtualAccount(100000, db.getAllSymbolDataDic())
    print "comm = ", va.calcComission(300)
    print "$ = ", va.getCash()
    print "pos = ", va.getAllPositions()
    va.buyAtMarket(3, 'XBB.TO', 100)
    print "pos = ", [p.toString() for p in va.getAllPositions()]
    va.buyAtMarket(6, 'XEC.TO', 200)
    print "pos = ", [p.toString() for p in va.getAllPositions()]
    va.sellAtMarket(va.getAllPositions()[0], 12)
    print "pos = ", [p.toString() for p in va.getAllPositions()]


if __name__ == '__main__':
    _main()
