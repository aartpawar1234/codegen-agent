import pytest
from calculator.advanced_operations import power, square_root


def test_power():
    assert power(2, 3) == 8
    assert power(5, 0) == 1
    assert power(0, 5) == 0


def test_square_root():
    assert square_root(4) == 2
    assert square_root(9) == 3
    with pytest.raises(ValueError):
        square_root(-1)
