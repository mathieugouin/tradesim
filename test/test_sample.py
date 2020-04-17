# content of test_sample.py
def func(x):
    return x + 1

def test_answer():
    assert func(3) == 4

def test_multi_answer():
    for i in range(100):
        assert func(i) == i + 1
