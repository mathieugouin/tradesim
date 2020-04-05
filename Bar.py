#-------------------------------------------------------------------------------
# Name:        Bar
# Purpose:
#-------------------------------------------------------------------------------

###############################################################################
class CBar:                  # P = Price
    """Represents a single financial stock data bar for one day."""
    def __init__(self, date, openP, highP, lowP, closeP, volume):
        self.date = date
        self.open = openP
        self.high = highP
        self.low = lowP
        self.close = closeP
        self.volume = volume

    def toString(self):
        return "D:{}, O:{}, H:{}, L:{}, C:{}, V:{}".format(
            self.date,
            self.open,
            self.high,
            self.low,
            self.close,
            self.volume)


def _main():
    import datetime
    bar = CBar(
                datetime.date.today(),
                10.0, # open
                15.0, # high
                9.0, # low
                12.0, # close
                123456 # volume (in nb of shares)
            )
    print bar.close
    print bar.toString()


if __name__ == '__main__':
    _main()
