# To make print working for Python2/3
from __future__ import print_function

class Position(object):
    """Represents a position held in a portfolio."""

    def __init__(self, bar, symbol, nbShare, price, name="buy", commission=9.95):
        """Equivalent to buy."""
        self._entryBar = bar
        self._entryPrice = price
        self._entryName = name
        self._entryCommission = commission

        self._exitBar = -1
        self._exitPrice = -1.0
        self._exitName = ""
        self._exitCommission = commission

        self._symbol = symbol
        self._nbShare = nbShare
        self._open = True

    def __str__(self):
        """Converts the Position to a string representation."""
        s = "Position " + self._symbol + " "
        s += "Open: bar={}, price={}, commission={}, name={}".format(
            self._entryBar,
            self._entryPrice,
            self._entryCommission,
            self._entryName
        )
        if not self._open:
            s += " Close: bar={}, price={}, commission={}, name={}, gain={}".format(
                self._exitBar,
                self._exitPrice,
                self._exitCommission,
                self._exitName,
                self.getPctGain()
            )
        return s

    def close(self, bar, price, name="sell"):
        if not self._open:
            print("Error: position already closed.")
        self._open = False
        self._exitPrice = price
        self._exitBar = bar
        self._exitName = name
        return self._nbShare * self._exitPrice

    def getSymbol(self):
        return self._symbol

    def getNbShare(self):
        return self._nbShare

    def isOpen(self):
        return self._open

    def getEntryPrice(self):
        return self._entryPrice

    def getExitPrice(self):
        return self._exitPrice

    def getPctGain(self):
        pc = 0
        if not self._open:
            entryCost = self._nbShare * self._entryPrice + self._entryCommission
            exitValue = self._nbShare * self._exitPrice - self._exitCommission
            pc = (exitValue - entryCost) / entryCost * 100
        else:
            print("ERROR: position still open")
        return pc


def _main():
    p1 = Position(3, 'XBB.TO', 10, 23.45)
    print(p1)
    print(p1.getSymbol())
    print(p1.getNbShare())
    print(p1.isOpen())
    print(p1.getEntryPrice())

    p1.close(4, 23.46)
    print(p1.getExitPrice())
    p2 = Position(6, 'XBB.TO', 10, 23.45, name='Test Pos', commission=0.1)
    p2.close(30, 25.68)
    print(p1)
    print(p2)


if __name__ == '__main__':
    _main()
