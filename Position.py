#-------------------------------------------------------------------------------
# Name:        Class Position
# Purpose:
#
#-------------------------------------------------------------------------------

###############################################################################
class CPosition:
    # Buy
    def __init__(self, bar, symbol, nbShare, price, name = "buy", commission = 9.95):
        self._entryBar          = bar
        self._entryPrice        = price
        self._entryName         = name
        self._entryCommission   = commission

        self._exitBar           = -1
        self._exitPrice         = -1.0
        self._exitName          = ""
        self._exitCommission    = commission

        self._symbol     = symbol
        self._nbShare    = nbShare
        self._open       = True

    def close(self, bar, price, name = "sell"):
        self._open      = False
        self._exitPrice = price
        self._exitBar   = bar
        self._exitName  = name
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
            print "ERROR: position still open"
        return pc

    def toString(self):
        return "TBD"

