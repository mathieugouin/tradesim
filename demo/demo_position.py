# To make print working for Python2/3
from __future__ import print_function

import position

def _main():
    p1 = position.Position(3, 'XBB.TO', 10, 23.45)
    print(p1)
    print(p1.get_symbol())
    print(p1.get_nb_share())
    print(p1.is_open())
    print(p1.get_entry_price())

    p1.close(4, 23.46)
    print(p1.get_exit_price())
    p2 = position.Position(6, 'XBB.TO', 10, 23.45, name='Test Pos', commission=0.1)
    p2.close(30, 25.68)
    print(p1)
    print(p2)


if __name__ == '__main__':
    _main()
