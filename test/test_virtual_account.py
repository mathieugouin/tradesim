import virtual_account as va
import stock_db_mgr as sdm


db = sdm.StockDBMgr('./stock_db/test')


def test_virtual_account():
    assert db
    a = va.VirtualAccount(100000.0, db.get_all_symbol_data())
    assert a

    assert a.get_cash() == 100000.0
    a.delta_cash(200)
    assert a.get_cash() == 100200.0
    a.delta_cash(-100)
    assert a.get_cash() == 100100.0

    assert len(a.get_all_positions()) == 0
    assert len(a.get_open_positions()) == 0
    assert len(a.get_close_positions()) == 0
    assert len(a.get_all_positions('SPY')) == 0
    assert len(a.get_open_positions('SPY')) == 0
    assert len(a.get_close_positions('SPY')) == 0

    a.buy_at_market(0, 'SPY', 100)

    assert len(a.get_all_positions()) == 1
    assert len(a.get_open_positions()) == 1
    assert len(a.get_close_positions()) == 0
    assert len(a.get_all_positions('SPY')) == 1
    assert len(a.get_open_positions('SPY')) == 1
    assert len(a.get_close_positions('SPY')) == 0
    assert len(a.get_all_positions('IBM')) == 0
    assert len(a.get_open_positions('IBM')) == 0
    assert len(a.get_close_positions('IBM')) == 0

    a.buy_at_market(1, 'IBM', 200)

    assert len(a.get_all_positions()) == 2
    assert len(a.get_open_positions()) == 2
    assert len(a.get_close_positions()) == 0
    assert len(a.get_all_positions('SPY')) == 1
    assert len(a.get_open_positions('SPY')) == 1
    assert len(a.get_close_positions('SPY')) == 0
    assert len(a.get_all_positions('IBM')) == 1
    assert len(a.get_open_positions('IBM')) == 1
    assert len(a.get_close_positions('IBM')) == 0

    a.sell_at_market(a.get_open_positions()[0], 12)

    assert len(a.get_all_positions()) == 2
    assert len(a.get_open_positions()) == 1
    assert len(a.get_close_positions()) == 1
    assert len(a.get_all_positions('SPY')) == 1
    assert len(a.get_open_positions('SPY')) == 0
    assert len(a.get_close_positions('SPY')) == 1
    assert len(a.get_all_positions('IBM')) == 1
    assert len(a.get_open_positions('IBM')) == 1
    assert len(a.get_close_positions('IBM')) == 0

    a.sell_at_market(a.get_open_positions()[0], 13)

    assert len(a.get_all_positions()) == 2
    assert len(a.get_open_positions()) == 0
    assert len(a.get_close_positions()) == 2
    assert len(a.get_all_positions('SPY')) == 1
    assert len(a.get_open_positions('SPY')) == 0
    assert len(a.get_close_positions('SPY')) == 1
    assert len(a.get_all_positions('IBM')) == 1
    assert len(a.get_open_positions('IBM')) == 0
    assert len(a.get_close_positions('IBM')) == 1


def test_too_expensive_buy():
    assert db
    c = 1000.0
    a = va.VirtualAccount(c, db.get_all_symbol_data())
    assert a
    a.buy_at_market(0, 'SPY', 2000)
    assert len(a.get_all_positions()) == 0
    assert a.get_cash() == c


def test_invalid_buy_qty():
    assert db
    c = 1000.0
    a = va.VirtualAccount(c, db.get_all_symbol_data())
    assert a
    a.buy_at_market(0, 'SPY', 0)
    assert len(a.get_all_positions()) == 0
    assert a.get_cash() == c
    a.buy_at_market(0, 'SPY', -10)
    assert len(a.get_all_positions()) == 0
    assert a.get_cash() == c


def test_invalid_sell():
    assert db
    c = 1000.0
    a = va.VirtualAccount(c, db.get_all_symbol_data())
    assert len(a.get_open_positions()) == 0
    assert a
    a.buy_at_market(0, 'SPY', 1)
    assert len(a.get_open_positions()) == 1
    p = a.get_open_positions()[0]
    a.sell_at_market(p, 1)
    c = a.get_cash()
    assert len(a.get_open_positions()) == 0
    a.sell_at_market(p, 2)  # 2nd invalid sell same position
    assert a.get_cash() == c


def test_too_expensive_sell():
    assert db
    c = 10000.0
    a = va.VirtualAccount(c, db.get_all_symbol_data())
    assert a
    a.buy_at_market(0, 'SPY', 1)
    assert len(a.get_open_positions()) == 1
    assert a.get_cash() < c
    a.delta_cash(-a.get_cash() + 0.1)
    assert a.get_cash() > 0.0
    c = a.get_cash()
    a.sell_at_market(a.get_open_positions()[0], 10)
    assert a.get_cash() == c
    assert len(a.get_open_positions()) == 1


def test_calc_commission():
    n = 1
    assert va.calc_commission(n) == 4.95 + 0.0035 * n
    n = 495
    assert va.calc_commission(n) == 4.95 + 0.0035 * n
    n = 5000
    assert va.calc_commission(n) == 9.95 + 0.0035 * n
