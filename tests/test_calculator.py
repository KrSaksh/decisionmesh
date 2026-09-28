import pytest

from decisionmesh.tools import Calculator


@pytest.fixture
def calculator():
    return Calculator()


def test_addition(calculator):
    assert calculator.calculate("2 + 3") == 5.0


def test_subtraction(calculator):
    assert calculator.calculate("10 - 4") == 6.0


def test_multiplication(calculator):
    assert calculator.calculate("6 * 7") == 42.0


def test_division(calculator):
    assert calculator.calculate("20 / 5") == 4.0


def test_operator_precedence(calculator):
    assert calculator.calculate("2 + 3 * 4") == 14.0


def test_parentheses(calculator):
    assert calculator.calculate("(2 + 3) * 4") == 20.0


def test_power(calculator):
    assert calculator.calculate("2 ** 3") == 8.0


def test_negative_numbers(calculator):
    assert calculator.calculate("-5 + 2") == -3.0


def test_division_by_zero(calculator):
    with pytest.raises(ValueError, match="divide by zero"):
        calculator.calculate("10 / 0")


def test_empty_expression(calculator):
    with pytest.raises(ValueError, match="cannot be empty"):
        calculator.calculate("")


def test_unsupported_expression(calculator):
    with pytest.raises(ValueError, match="Unsupported expression"):
        calculator.calculate("abs(-5)")