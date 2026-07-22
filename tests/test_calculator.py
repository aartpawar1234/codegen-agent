import pytest
from calculator.calculator import Calculator


def test_calculator_operations():
    calc = Calculator()
    assert calc.calculate('add', 1, 2) == 3
    assert calc.calculate('subtract', 5, 3) == 2
    assert calc.calculate('multiply', 3, 4) == 12
    assert calc.calculate('divide', 10, 2) == 5
    assert calc.calculate('power', 2, 3) == 8
    assert calc.calculate('square_root', 4) == 2
    with pytest.raises(ValueError):
        calc.calculate('divide', 1, 0)
    with pytest.raises(ValueError):
        calc.calculate('unknown', 1, 2)
