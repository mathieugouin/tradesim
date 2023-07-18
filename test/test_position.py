import pytest
import re
import position


def test_position_default():
    p = position.Position(3, 'XBB.TO', 100, 20.0)
    s1 = str(p)
    assert len(s1) > 0
    assert re.search('buy', s1)
    assert re.search('sell', s1) is None
    assert p.get_symbol() == 'XBB.TO'
    assert p.get_nb_share() == 100
    assert p.is_open()
    assert p.get_entry_price() == 20.0
    assert p.get_pct_gain() == 0.0

    c = p.close(4, 25.0)
    assert not p.is_open()
    assert p.close(5, 30.0) == c
    assert not p.is_open()
    s2 = str(p)
    assert len(s2) > len(s1)
    assert re.search('buy', s2)
    assert re.search('sell', s2)
    assert p.get_exit_price() == 25.0
    assert 0.0 < p.get_pct_gain() < 100.0


def test_position_custom_arg():
    open_name = 'Test Pos Open'
    close_name = 'Test Pos Close'

    p = position.Position(6, 'ZCN.TO', 1000, 23.45, name=open_name, commission=0.1)

    s1 = str(p)
    assert len(s1) > 0
    assert re.search(open_name, s1)
    assert re.search(close_name, s1) is None

    _ = p.close(7, 25.68, name=close_name)
    s2 = str(p)

    assert len(s2) > len(s1)
    assert re.search(open_name, s2)
    assert re.search(close_name, s2)
