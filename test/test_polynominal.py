import pytest
from polynominal import PolynomialTerm, PolynomParser, Polynomial


data_polynom_term_positive_string = [
    {"input": "-0", "expected": PolynomialTerm(0, 0)},
    {"input": "+0", "expected": PolynomialTerm(0, 0)},
    {"input": "0", "expected": PolynomialTerm(0, 0)},
    {"input": "X", "expected": PolynomialTerm(1, 1)},
    {"input": "+X", "expected": PolynomialTerm(1, 1)},
    {"input": "-X", "expected": PolynomialTerm(-1, 1)},
    {"input": "+4", "expected": PolynomialTerm(4, 0)},
    {"input": "4", "expected": PolynomialTerm(4, 0)},
    {"input": "-5", "expected": PolynomialTerm(-5, 0)},
    {"input": "X^2", "expected": PolynomialTerm(1, 2)},
    {"input": "-X^2", "expected": PolynomialTerm(-1, 2)},
    {"input": "2*X", "expected": PolynomialTerm(2, 1)},
    {"input": "+2*X", "expected": PolynomialTerm(2, 1)},
    {"input": "-2*X", "expected": PolynomialTerm(-2, 1)},
    {"input": "3*X^2", "expected": PolynomialTerm(3, 2)},
    {"input": "+3*X^2", "expected": PolynomialTerm(3, 2)},
    {"input": "-3*X^2", "expected": PolynomialTerm(-3, 2)},
    {"input": "X^3", "expected": PolynomialTerm(1, 3)},
    {"input": "+X^3", "expected": PolynomialTerm(1, 3)},
    {"input": "-X^3", "expected": PolynomialTerm(-1, 3)},
    {"input": "5*X^4", "expected": PolynomialTerm(5, 4)},
    {"input": "+5*X^4", "expected": PolynomialTerm(5, 4)},
    {"input": "-5*X^4", "expected": PolynomialTerm(-5, 4)},
]


@pytest.mark.parametrize("term_data", data_polynom_term_positive_string)
def test_polynomial_term_from_string_positive(term_data):
    term_str = term_data["input"]
    expected_term = term_data["expected"]
    term = PolynomialTerm.from_string(term_str)
    assert term.coefficient == expected_term.coefficient
    assert term.degree == expected_term.degree


def test_polynomial_term_eq():
    term1 = PolynomialTerm(1, 2)
    term2 = PolynomialTerm(1, 2)
    assert term1 == term2
    term1 = PolynomialTerm(1, 2)
    term2 = PolynomialTerm(1, 3)
    assert term1 != term2


def test_polynomial_term_repr():
    term = PolynomialTerm(1, 2)
    assert repr(term) == "PolynomialTerm(1, 2)"


def test_polynomial_term_str():
    term = PolynomialTerm(1, 2)
    assert str(term) == "1*X^2"
    term = PolynomialTerm(0, 2)
    assert str(term) == "0*X^2"
    term = PolynomialTerm(-1, 2)
    assert str(term) == "-1*X^2"
    term = PolynomialTerm(1, 0)
    assert str(term) == "1*X^0"
    term = PolynomialTerm(0, 0)
    assert str(term) == "0*X^0"
    term = PolynomialTerm(-1, 0)
    assert str(term) == "-1*X^0"


data_polynom_parser_positive_string = [
    {"input": "0=0", "expected": [PolynomialTerm(0, 0), PolynomialTerm(0, 0)]},
    {"input": "X=0", "expected": [PolynomialTerm(1, 1), PolynomialTerm(0, 0)]},
    {"input": "X^2=0", "expected": [PolynomialTerm(1, 2), PolynomialTerm(0, 0)]},
    {"input": "X^2+X=0", "expected": [PolynomialTerm(1, 2), PolynomialTerm(1, 1), PolynomialTerm(0, 0)]},
    {"input": "X^2+X^3=0", "expected": [PolynomialTerm(1, 2), PolynomialTerm(1, 3), PolynomialTerm(0, 0)]},
    {"input": "X^2+X^3+X=-1", "expected": [PolynomialTerm(1, 2), PolynomialTerm(1, 3), PolynomialTerm(1, 1), PolynomialTerm(1, 0)]},
    {"input": "2*X^2+3*X^3+4*X^4-1=0", "expected": [PolynomialTerm(2, 2), PolynomialTerm(3, 3), PolynomialTerm(4, 4), PolynomialTerm(-1, 0), PolynomialTerm(0, 0)]},
    # String with spaces. Normalization test
    {"input": "  2 *X ^ 2+ 3* X ^3+ 4 * x ^ 4 -1 = 0  ", "expected": [PolynomialTerm(2, 2), PolynomialTerm(3, 3), PolynomialTerm(4, 4), PolynomialTerm(-1, 0), PolynomialTerm(0, 0)]},
    ]


@pytest.mark.parametrize("polynom_data", data_polynom_parser_positive_string)
def test_polynomial_parser_positive(polynom_data):
    polynom_str = polynom_data["input"]
    expected_polynom = polynom_data["expected"]
    polynom = PolynomParser.parse(polynom_str)
    assert polynom == expected_polynom


data_polynom_parser_negative_string = [
    {"input": "abc", "expected": "Invalid polynomial string"},
    {"input": "X=abc", "expected": "Invalid polynomial string"},
    {"input": "X=0=0", "expected": "Invalid polynomial string"},
    {"input": "2X2X=3X", "expected": "Invalid term"},
    {"input": "=3*X", "expected": "Invalid polynomial string"},
    {"input": "X=^2", "expected": "Invalid term"},
    {"input": "X++2=0", "expected": "Invalid polynomial string"},
    {"input": "X--2=0", "expected": "Invalid polynomial string"},
    {"input": "X+=0", "expected": "Invalid polynomial string"},
    {"input": "X-=0", "expected": "Invalid polynomial string"},
    {"input": "2*X*3=0", "expected": "Invalid term"},
    {"input": "X*X=0", "expected": "Invalid term"},
    {"input": "=X=0", "expected": "Invalid polynomial string"},
    {"input": "X==0", "expected": "Invalid polynomial string"},
    {"input": "=X=2", "expected": "Invalid polynomial string"},
    {"input": "X=", "expected": "Invalid polynomial string"},
    {"input": "=X", "expected": "Invalid polynomial string"},
    {"input": "X+*2=0", "expected": "Invalid term"},
    {"input": "X*+2=0", "expected": "Invalid term"},
    {"input": "*X*2=0", "expected": "Invalid term"}]


@pytest.mark.parametrize("polynom_data", data_polynom_parser_negative_string)
def test_polynomial_parser_negative(polynom_data):
    polynom_str = polynom_data["input"]
    expected_error_message = polynom_data["expected"]
    with pytest.raises(Exception) as e:
        PolynomParser.parse(polynom_str)
    assert expected_error_message in str(e.value)


def test_polynomial(monkeypatch):
    terms = [PolynomialTerm(1, 2), PolynomialTerm(1, 3), PolynomialTerm(1, 4)]
    monkeypatch.setattr(Polynomial, "__abstractmethods__", set())
    polynom = Polynomial(terms)
    assert polynom.terms == terms
    assert polynom.degree == 4