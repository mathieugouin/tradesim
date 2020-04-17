import virtual_account as va
import stock_db_mgr as sdm


def __print_position(va):
    print("all pos = {}".format([str(p) for p in va.get_all_positions()]))
    print("open pos = {}".format([str(p) for p in va.get_open_positions()]))
    print("closed pos = {}".format([str(p) for p in va.get_close_positions()]))

    print("all pos (XBB.TO) = {}".format([str(p) for p in va.get_all_positions('XBB.TO')]))
    print("open pos (XBB.TO) = {}".format([str(p) for p in va.get_open_positions('XBB.TO')]))
    print("closed pos (XBB.TO) = {}".format([str(p) for p in va.get_close_positions('XBB.TO')]))


def test_answer():
    db = sdm.StockDBMgr('./stock_db/test')
    va = VirtualAccount(100000, db.get_all_symbol_data())
    assert db
    assert va

    assert va.get_cash() == 100000.0
    va.delta_cash(200)
    assert va.get_cash() == 100200.0
    va.delta_cash(-100)
    assert va.get_cash() == 100100.0

    assert len(va.get_all_positions()) == 0
    assert len(va.get_open_positions()) == 0
    assert len(va.get_close_positions()) == 0
    assert len(va.get_all_positions('SPY')) == 0
    assert len(va.get_open_positions('SPY')) == 0
    assert len(va.get_close_positions('SPY')) == 0

    va.buy_at_market(3, 'SPY', 100)

    assert len(va.get_all_positions()) == 1
    assert len(va.get_open_positions()) == 1
    assert len(va.get_close_positions()) == 0
    assert len(va.get_all_positions('SPY')) == 1
    assert len(va.get_open_positions('SPY')) == 1
    assert len(va.get_close_positions('SPY')) == 0
    assert len(va.get_all_positions('IBM')) == 0
    assert len(va.get_open_positions('IBM')) == 0
    assert len(va.get_close_positions('IBM')) == 0

    va.buy_at_market(6, 'IBM', 200)

    assert len(va.get_all_positions()) == 2
    assert len(va.get_open_positions()) == 2
    assert len(va.get_close_positions()) == 0
    assert len(va.get_all_positions('SPY')) == 1
    assert len(va.get_open_positions('SPY')) == 1
    assert len(va.get_close_positions('SPY')) == 0
    assert len(va.get_all_positions('IBM')) == 1
    assert len(va.get_open_positions('IBM')) == 1
    assert len(va.get_close_positions('IBM')) == 0

    va.sell_at_market(va.get_open_positions()[0], 12)

    assert len(va.get_all_positions()) == 2
    assert len(va.get_open_positions()) == 1
    assert len(va.get_close_positions()) == 1
    assert len(va.get_all_positions('SPY')) == 1
    assert len(va.get_open_positions('SPY')) == 0
    assert len(va.get_close_positions('SPY')) == 1
    assert len(va.get_all_positions('IBM')) == 1
    assert len(va.get_open_positions('IBM')) == 1
    assert len(va.get_close_positions('IBM')) == 0

    va.sell_at_market(va.get_open_positions()[0], 13)

    assert len(va.get_all_positions()) == 2
    assert len(va.get_open_positions()) == 0
    assert len(va.get_close_positions()) == 2
    assert len(va.get_all_positions('SPY')) == 1
    assert len(va.get_open_positions('SPY')) == 0
    assert len(va.get_close_positions('SPY')) == 1
    assert len(va.get_all_positions('IBM')) == 1
    assert len(va.get_open_positions('IBM')) == 0
    assert len(va.get_close_positions('IBM')) == 1


def test_calc_commission():
    n = 1
    assert calc_commission(n) == 4.95 + 0.0035 * n
    n = 495
    assert calc_commission(n) == 4.95 + 0.0035 * n
    n = 5000
    assert calc_commission(n) == 9.95 + 0.0035 * n

