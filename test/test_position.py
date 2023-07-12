import pytest
import position


@pytest.mark.toimprove
def test_position_default():
    p = position.Position(3, 'XBB.TO', 100, 20.0)
    assert len(str(p)) > 0  # TBD
    assert p.get_symbol() == 'XBB.TO'
    assert p.get_nb_share() == 100
    assert p.is_open()
    assert p.get_entry_price() == 20.0
    assert p.get_pct_gain() == 0.0

    c = p.close(4, 25.0)
    assert not p.is_open()
    assert p.close(5, 30.0) == c
    assert not p.is_open()
    assert len(str(p)) > 0  # TBD
    assert p.get_exit_price() == 25.0
    assert 0.0 < p.get_pct_gain() < 100.0


@pytest.mark.toimprove
def test_position_custom_arg():
    p = position.Position(6, 'ZCN.TO', 1000, 23.45, name='Test Pos Open', commission=0.1)
    p.close(7, 25.68, name='Test Pos Close')
    assert len(str(p)) > 0  # TBD
