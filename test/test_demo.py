# simple demo unit test


def func(x):
    return x + 1


def test_call():
    assert func(3) == 4


def test_multi_call():
    for i in range(100):
        assert func(i) == i + 1
