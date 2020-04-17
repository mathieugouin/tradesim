import position


def test_position_1():
    p = position.Position(3, 'XBB.TO', 100, 20.0)
    assert len(str(p)) > 0  # TBD
    assert p.get_symbol() == 'XBB.TO'
    assert p.get_nb_share() == 100
    assert p.is_open()
    assert p.get_entry_price() == 20.0

    p.close(4, 25.0)
    assert len(str(p)) > 0  # TBD
    assert p.get_exit_price() == 25.0
    assert 0.0 < p.get_pct_gain() < 100.0


def test_position_2():
    p = position.Position(6, 'ZCN.TO', 1000, 23.45, name='Test Pos', commission=0.1)
    p.close(7, 25.68)
    assert len(str(p)) > 0  # TBD
