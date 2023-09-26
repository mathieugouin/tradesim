import pytest


def my_coverage(x):
    a = None

    if x == 0:
        a = 0

    if x > 0:
        a = 1

    if x < 0:
        a = -1

    return a


def my_sum(a, b):
    return a + b


def exception_function(x):
    if x <= 0:
        raise AssertionError("x must be greater than 0")
    return x + 1


@pytest.mark.dummytest
@pytest.mark.parametrize("x", [0, 1, -1])
def test_coverage_1(x):
    assert my_coverage(x) is not None


# Sequential
@pytest.mark.dummytest
@pytest.mark.parametrize("a, b, s", [
    (1, 1, 2),
    (1, 2, 3),
    (2, 2, 4),
])
def test_param_1(a, b, s):
    assert my_sum(a, b) == s


# Combinatorial
@pytest.mark.dummytest
@pytest.mark.parametrize("a", [1, 2])
@pytest.mark.parametrize("b", [11, 12, 13])
@pytest.mark.parametrize("s", [101, 102, 103, 104])
def test_param_2(a, b, s):
    assert my_sum(a, b) < s


@pytest.mark.dummytest
@pytest.mark.webtest
def test_webtest_1():
    assert my_sum(2, 2) == 4


@pytest.mark.dummytest
@pytest.mark.webtest
def test_webtest_2():
    assert my_sum(2, 2) == 4


@pytest.mark.dummytest
@pytest.mark.smoketest
def test_smoketest_1():
    assert my_sum(2, 2) == 4


@pytest.mark.dummytest
@pytest.mark.smoketest
def test_smoketest_2():
    assert my_sum(2, 2) == 4


@pytest.mark.dummytest
@pytest.mark.toimprove
def test_toimprove():
    assert my_sum(2, 2) == 4


@pytest.mark.dummytest
def test_print_pass():
    print("test_print_pass should pass...")
    assert my_sum(2, 2) == 4


@pytest.mark.dummytest
def test_no_exception():
    assert 2 == exception_function(1)


@pytest.mark.dummytest
def test_exception():
    with pytest.raises(AssertionError):
        exception_function(0)


@pytest.mark.xfail(reason="This test is known to fail")
@pytest.mark.dummytest
def test_known_failure():
    assert my_sum(2, 2) == 5
