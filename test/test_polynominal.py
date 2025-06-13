import pytest
from polynominal import PolynomSecondDegree, PolynomTerm, PolynomParser


# def test_discriminant_property():
#     poly = PolynomSecondDegree(1, -3, 2)
#     # discriminant = (-3)^2 - 4*1*2 = 9 - 8 = 1
#     assert poly.discriminant == 1

# def test_solutions_count_two():
#     poly = PolynomSecondDegree(1, 0, -1)  # x^2 - 1 = 0, discriminant = 4 > 0
#     assert poly.sulutions_count() == 2

# def test_solutions_count_one():
#     poly = PolynomSecondDegree(1, 2, 1)  # x^2 + 2x + 1 = 0, discriminant = 0
#     assert poly.sulutions_count() == 1

# def test_solutions_count_zero():
#     poly = PolynomSecondDegree(1, 0, 1)  # x^2 + 1 = 0, discriminant = -4 < 0
#     assert poly.sulutions_count() == 0

# def test_polynomparser_normalize_valid():
#     parser = PolynomParser("2 * X^2 + 3 * X + 1 = 0")
#     assert isinstance(parser.polynom_str, str)

# def test_polynomparser_normalize_invalid():
#     with pytest.raises(ValueError):
#         PolynomParser("2 * X^2 + 3 * X + 1 = a")

# def test_polynomparser_normalize_not_string():
#     with pytest.raises(ValueError):
#         PolynomParser(12345)

data_polynomterm_from_string = [
    {"input": "0", "expected": PolynomTerm(0, 0)},
    {"input": "X", "expected": PolynomTerm(1, 1)},
    {"input": "-X", "expected": PolynomTerm(-1, 1)},
    {"input": "4", "expected": PolynomTerm(4, 0)},
    {"input": "-5", "expected": PolynomTerm(-5, 0)},
    {"input": "2*X", "expected": PolynomTerm(2, 1)},
    {"input": "-2*X", "expected": PolynomTerm(-2, 1)},
    {"input": "3*X^2", "expected": PolynomTerm(3, 2)},
    {"input": "-3*X^2", "expected": PolynomTerm(-3, 2)},
    {"input": "X^3", "expected": PolynomTerm(1, 3)},
    {"input": "-X^3", "expected": PolynomTerm(-1, 3)},
    {"input": "5*X^4", "expected": PolynomTerm(5, 4)},
    {"input": "-5*X^4", "expected": PolynomTerm(-5, 4)},
]

@pytest.mark.parametrize("term_data", data_polynomterm_from_string)
def test_polynomterm_from_string(term_data):
    term_str = term_data["input"]
    expected_term = term_data["expected"]
    term = PolynomTerm.from_string(term_str)
    assert term.coefficient == expected_term.coefficient
    assert term.degree == expected_term.degree