import parent_import
import virtual_account as va
import finance_utils as fu
import stock_db_mgr as sdm


def __print_position(account):
    print("all pos = {}".format([str(p) for p in account.get_all_positions()]))
    print("open pos = {}".format([str(p) for p in account.get_open_positions()]))
    print("closed pos = {}".format([str(p) for p in account.get_close_positions()]))

    print("all pos (XBB.TO) = {}".format([str(p) for p in account.get_all_positions('XBB.TO')]))
    print("open pos (XBB.TO) = {}".format([str(p) for p in account.get_open_positions('XBB.TO')]))
    print("closed pos (XBB.TO) = {}".format([str(p) for p in account.get_close_positions('XBB.TO')]))


def __main():
    db = sdm.StockDBMgr('stock_db/qt')
    account = va.VirtualAccount(100000, db.get_all_symbol_data())
    print("comm = {}".format(fu.calc_commission(300)))
    print("$ = {}".format(account.get_cash()))
    account.delta_cash(100)
    print("$ = {}".format(account.get_cash()))
    account.delta_cash(-200)
    print("$ = {}".format(account.get_cash()))
    __print_position(account)
    account.buy_at_market(3, 'XBB.TO', 100)
    __print_position(account)
    account.buy_at_market(6, 'XEC.TO', 200)
    __print_position(account)
    account.sell_at_market(account.get_all_positions()[0], 12)
    __print_position(account)


if __name__ == '__main__':
    __main()
