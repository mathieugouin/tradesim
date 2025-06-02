"""Module to define the Position class."""


class Position(object):
    """Represents a position held in a portfolio."""

    def __init__(self, bar, symbol, nb_share, price, name="buy", commission=9.95):
        """Creating a Position is equivalent to buy."""
        self._entry_bar = bar
        self._entry_price = price
        self._entry_name = name
        self._entry_commission = commission

        self._exit_bar = -1
        self._exit_price = -1.0
        self._exit_name = ""
        self._exit_commission = commission

        self._symbol = symbol
        self._nb_share = nb_share
        self._open = True

    def __str__(self):
        """Converts the Position to a string representation."""
        s = "Position " + self._symbol + " "
        s += "Open: bar={}, price={}, commission={}, name={}".format(
            self._entry_bar,
            self._entry_price,
            self._entry_commission,
            self._entry_name
        )
        if not self._open:
            s += " Close: bar={}, price={}, commission={}, name={}, gain={}".format(
                self._exit_bar,
                self._exit_price,
                self._exit_commission,
                self._exit_name,
                self.get_pct_gain()
            )
        return s

    def close(self, bar, price, name="sell"):
        if self._open:
            self._open = False
            self._exit_price = price
            self._exit_bar = bar
            self._exit_name = name
        else:
            raise AssertionError("Position already closed.")
        return self._nb_share * self._exit_price

    def get_symbol(self):
        return self._symbol

    def get_nb_share(self):
        return self._nb_share

    def is_open(self):
        return self._open

    def get_entry_price(self):
        return self._entry_price

    def get_exit_price(self):
        return self._exit_price

    def get_pct_gain(self):
        pc = 0
        if not self._open:
            entry_cost = self._nb_share * self._entry_price + self._entry_commission
            exit_value = self._nb_share * self._exit_price - self._exit_commission
            pc = (exit_value - entry_cost) / entry_cost * 100
        else:
            raise AssertionError("Position still open")
        return pc
