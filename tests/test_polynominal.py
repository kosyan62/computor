import re

import pytest
from polynominal import PolynomialTerm, PolynomParser, Polynomial, PolynomialFactory
from test_data import (
    data_polynom_term_positive_tuple,
    data_polynom_parser_positive_string,
    data_polynom_parser_negative_string,
    data_polynom_second_degree_positive_tuple,
    ids_polynom_second_degree_positive,
    data_polynom_second_degree_reduce_positive_string,
    data_polynom_first_degree_positive_tuple,
    data_polynom_first_degree_negative_tuple,
    data_polynom_second_degree_all_positive_tuple,
)


@pytest.mark.parametrize("term_str,expected", data_polynom_term_positive_tuple)
def test_polynomial_term_from_string_positive(term_str, expected):
    term = PolynomialTerm.from_string(term_str)
    assert term.coefficient == expected.coefficient
    assert term.degree == expected.degree


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


@pytest.mark.parametrize("polynom_data", data_polynom_parser_positive_string)
def test_polynomial_parser_positive(polynom_data):
    polynom_str = polynom_data["input"]
    expected_polynom = polynom_data["expected"]
    polynom = PolynomParser.parse(polynom_str)
    assert polynom == expected_polynom


@pytest.mark.parametrize("polynom_data", data_polynom_parser_negative_string)
def test_polynomial_parser_negative(polynom_data):
    polynom_str = polynom_data["input"]
    expected_error_message = polynom_data["expected"]
    with pytest.raises(Exception) as e:
        PolynomParser.parse(polynom_str)
    assert expected_error_message in str(e.value)


def test_polynomial(monkeypatch):
    terms = [
        PolynomialTerm(4, 4),
        PolynomialTerm(2, 3),
        PolynomialTerm(1, 2),
    ]
    terms_result = [
        PolynomialTerm(0, 0),
        PolynomialTerm(0, 1),
        PolynomialTerm(1, 2),
        PolynomialTerm(2, 3),
        PolynomialTerm(4, 4),
    ]
    monkeypatch.setattr(Polynomial, "__abstractmethods__", set())
    polynom = Polynomial(terms)  # noqa
    assert polynom.terms == terms_result
    assert polynom.degree == 4


@pytest.mark.parametrize(
    "equation,discriminant,roots",
    data_polynom_second_degree_positive_tuple,
    ids=ids_polynom_second_degree_positive,
)
def test_polynomial_2nd_functional(equation, discriminant, roots):
    polynomial = PolynomialFactory(PolynomParser).create(equation)
    assert polynomial.degree == 2, "Wrong degree"
    assert polynomial.discriminant == discriminant, "Wrong discriminant"
    assert polynomial.solutions_count == len(roots), "Wrong solutions count"

    solutions = set(polynomial.get_solutions())
    assert roots == solutions, "Wrong solutions"


def test_polynomial_2nd_one_root():
    roots = {0.0}
    polynominal = PolynomialFactory(PolynomParser).create("1x^2 + 0x + 0 = 0")
    assert polynominal.degree == 2, "Wrong degree"
    assert polynominal.discriminant == 0, "Wrong discriminant"
    assert polynominal.solutions_count == 1, "Wrong solutions count"
    solutions = set(polynominal.get_solutions())
    assert roots == solutions, "Wrong solutions"


def test_polynomial_2nd_complex():
    roots = {-0.5 + 0.5j, -0.5 - 0.5j}
    polynominal = PolynomialFactory(PolynomParser).create("6x^2 + 6x + 3 = 0")
    assert polynominal.degree == 2, "Wrong degree"
    assert polynominal.discriminant == -36, "Wrong discriminant"
    assert polynominal.solutions_count == 2, "Wrong solutions count"
    solutions = set(polynominal.get_solutions())
    assert roots == solutions, "Wrong solutions"


@pytest.mark.parametrize(
    "polynom_data", data_polynom_second_degree_reduce_positive_string
)
def test_polynomial_2nd_reduce(polynom_data):
    polynom_str = polynom_data["input"]
    expected_polynom = polynom_data["expected"]
    polynom = PolynomialFactory(PolynomParser).create(polynom_str)
    assert polynom.get_reduced_form() == expected_polynom, "Wrong reduce"


@pytest.mark.parametrize("equation,root", data_polynom_first_degree_positive_tuple)
def test_polynomial_1st_degree(equation, root):
    polynominal = PolynomialFactory(PolynomParser).create(equation)
    assert polynominal.degree == 1, "Wrong degree"
    # assert polynominal.solutions_count == 1, "Wrong solutions count"
    solutions = set(polynominal.get_solutions())
    assert solutions == {root}, "Wrong solutions"


@pytest.mark.parametrize(
    "equation,solutions_count", data_polynom_first_degree_negative_tuple
)
def test_polynomial_1st_degree_negative(equation, solutions_count):
    polynominal = PolynomialFactory(PolynomParser).create(equation)
    assert polynominal.degree == 1, "Wrong degree"
    assert polynominal.solutions_count == solutions_count, "Wrong solutions count"
    assert polynominal.get_solutions() == (), "Wrong solutions"


@pytest.mark.parametrize(
    "equation,discriminant,roots", data_polynom_second_degree_all_positive_tuple
)
def test_polynomial_2nd_functional_all_positive(equation, discriminant, roots):
    polynomial = PolynomialFactory(PolynomParser).create(equation)
    assert polynomial.degree == 2, "Wrong degree"
    assert polynomial.discriminant == discriminant, "Wrong discriminant"
    solutions = polynomial.get_solution_string().replace(" ", "").replace("x=", "")
    roots = roots.replace(" ", "").replace("x=", "")
    assert polynomial.solutions_count == len(roots.split(",")), "Wrong solutions count"

    roots_arr = re.split("[-,+]", roots)
    solutions_arr = re.split("[-,+]", solutions)
    assert set(solutions_arr) == set(roots_arr), "Wrong solutions"
    assert roots.count(",") == solutions.count(","), "Wrong solutions count"
    assert roots.count("+") == solutions.count("+"), "Wrong sign in solutions"
    assert roots.count("-") == solutions.count("-"), "Wrong sign in solutions"


def test_polynomial_0_degree():
    polynominal = PolynomialFactory(PolynomParser).create("1 = 1")
    assert polynominal.degree == 0, "Wrong degree"
    assert polynominal.solutions_count == float("inf"), "Wrong solutions count"
    assert "Any X is solution" == polynominal.get_solution_string(), "Wrong solutions"

    polynominal = PolynomialFactory(PolynomParser).create("1 = 0")
    assert polynominal.degree == 0, "Wrong degree"
    assert polynominal.solutions_count == -1, "Wrong solutions count"
    assert "The sides of equation are not equal. Cannot solve." == polynominal.get_solution_string(), "Wrong solutions"
