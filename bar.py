# To make print working for Python2/3
from __future__ import print_function

class Bar(object):
    """Represents a single financial stock data bar for one day."""
    def __init__(self, date, openP, highP, lowP, closeP, volume):
        # P = Price
        self.date = date
        self.open = openP
        self.high = highP
        self.low = lowP
        self.close = closeP
        self.volume = volume

    def __str__(self):
        return "D:{}, O:{}, H:{}, L:{}, C:{}, V:{}".format(
            self.date,
            self.open,
            self.high,
            self.low,
            self.close,
            self.volume)


def _main():
    import datetime
    bar = Bar(
                datetime.date.today(),
                10.0, # open
                15.0, # high
                9.0, # low
                12.0, # close
                123456 # volume (in nb of shares)
            )
    print(bar.close)
    print(bar)


if __name__ == '__main__':
    _main()