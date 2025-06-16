import re
from abc import ABC, abstractmethod
from typing import List, Tuple


class PolynomialTerm:
    def __init__(self, coefficient, degree):
        self.coefficient = coefficient
        self.degree = degree

    @classmethod
    def from_string(cls, term_str: str):
        """Create a PolynomTerm from a string representation."""
        original_str = term_str
        if not isinstance(term_str, str):
            raise ValueError("Invalid term string: not a string.")
        if "X" not in term_str:
            term_str += "*X^0"
        if term_str.endswith("X"):
            term_str += "^1"
        if term_str.startswith("X") or term_str.startswith("+X"):
            term_str = "1*" + term_str
        elif term_str.startswith("-X"):
            term_str = "-1*" + term_str[1:]

        if term_str.count("*") != 1 or term_str.count(
                "^") != 1 or term_str.count("X") != 1:
            raise ValueError(f"Invalid term - \"{original_str}\": invalid format.")
        coefficient, degree = term_str.split("*")
        coefficient = int(coefficient)
        degree = int(degree.replace("X^", ""))
        return cls(coefficient, degree)

    def __str__(self):
        return f"{self.coefficient}*X^{self.degree}"

    def __repr__(self):
        return f"PolynomialTerm({self.coefficient}, {self.degree})"

    def __eq__(self, other):
        return self.degree == other.degree and self.coefficient == other.coefficient


class Polynomial(ABC):
    """
    Representation of a general polynomial using terms with coefficients and degrees.
    """

    def __init__(self, terms: List[PolynomialTerm]):
        """
        Represents a polynomial equation using a list of polynomial terms.

        This class initializes with a list of PolynomialTerm objects, which represent
        the individual terms of a polynomial. It ensures that terms are sorted by their
        degree and performs a reduction step to simplify the polynomial by combining
        like terms if applicable.

        :param terms: Dictionary of terms in the polynomial.
        :type terms: List[PolynomialTerm]
        """
        self._degree = None
        self._solutions_count = None
        self._terms = None

        # setting
        self.terms = terms
        self.degree  # noqa

    @property
    @abstractmethod
    def solutions_count(self) -> int:
        """Returns the number of solutions for the polynomial."""
        raise NotImplementedError

    @abstractmethod
    def get_reduced_form(self):
        """Returns the reduced form of the polynomial."""
        raise NotImplementedError

    @abstractmethod
    def get_solutions(self) -> Tuple[float]:
        """Returns the solutions for the polynomial."""
        raise NotImplementedError

    @property
    def degree(self):
        """Returns the degree of the polynomial."""
        if not self._degree:
            self._degree = self.find_max_degree(self.terms)
        return self._degree

    @property
    def terms(self):
        return self._terms

    @terms.setter
    def terms(self, value: List[PolynomialTerm]) -> None:
        """
        Sets the terms of the polynomial while reducing terms to the same degree by
        combining their coefficients.

        This setter method processes the list of polynomial terms and consolidates duplicate
        terms by degree, ensuring that each degree has a single term with a summed coefficient.

        :param value: A list of polynomial terms to be set in the polynomial. Each term
            is an instance of the PolynomialTerm class and contains a degree and
            coefficient.
        :type value: List[PolynomialTerm]
        :return: None
        """
        if self.terms:
            raise ValueError("Terms cannot be set after initialization.")
        if not isinstance(value, list):
            raise ValueError(
                "Value of terms must be a list of PolynomialTerm objects.")
        reduced_terms = {}
        for term in value:
            if not isinstance(term, PolynomialTerm):
                raise ValueError(
                    "Value of terms must be a list of PolynomialTerm objects.")
            if term.degree not in reduced_terms.keys():
                reduced_terms[term.degree] = term
            else:
                reduced_terms[term.degree].coefficient += term.coefficient

        self._terms = sorted(reduced_terms.values(), key=lambda x: x.degree)

    @staticmethod
    def find_max_degree(terms: List[PolynomialTerm]) -> int:
        """Returns the highest degree among all polynomial terms.

        Args:
            terms: List of polynomial terms

        Returns:
            The maximum degree value found in terms
        """
        return max((term.degree for term in terms), default=0)


class PolynomialFactory:
    """Factory class for creating polynomials of different degrees."""

    def __init__(self, parser):
        self.parser = parser
        self.polynomials = {
            1: PolynomialFirstDegree,
            2: PolynomialSecondDegree
        }

    def create(self, polynom_str):
        """Create a polynomial object based on the polynomial string."""
        polynom_terms = self.parser.parse(polynom_str)
        degree = self.parser.degree
        if degree not in self.polynomials.keys():
            raise ValueError(f"Polynomial of degree {degree} is not supported.")
        return self.polynomials[degree](polynom_terms)


class PolynomialFirstDegree(Polynomial):
    def __init__(self, terms):
        super().__init__(terms)


class PolynomialSecondDegree(Polynomial):
    def __init__(self, terms):
        super().__init__(terms)
        self._discriminant = None


class PolynomParser:
    pattern = r"^[\dX\^\-\+\*=]+$"  # Regex pattern to match a polynomial string

    @classmethod
    def normalize(cls, polynom_str: str):
        """Normalize and validate a polynomial string."""
        if not isinstance(polynom_str, str):
            raise ValueError(
                "Invalid polynomial string to parse: not a string.")
        if polynom_str.count("=") != 1:
            raise ValueError(
                "Invalid polynomial string to parse: '=' should be present exactly once.")
        if polynom_str.startswith("=") or polynom_str.endswith("="):
            raise ValueError(
                "Invalid polynomial string to parse: '=' should not be at the beginning or end.")
        polynom_str = polynom_str.strip()
        polynom_str = polynom_str.replace("\n", "")
        polynom_str = polynom_str.replace(" ", "")
        polynom_str = polynom_str.replace("x", "X")
        if re.match(cls.pattern, polynom_str) is None:
            raise ValueError(
                "Invalid polynomial string to parse: contains invalid characters.")
        return polynom_str

    @classmethod
    def parse(cls, polynomial_str: str):
        """Parse a polynomial string into a list of PolynomialTerm objects."""
        polynomial_str = cls.normalize(polynomial_str)
        # Now we need to transfer terms from after equal sign to before with sign change
        polynomial_left, polynomial_right = polynomial_str.split("=")

        # Split the polynomial string into parts based on operators
        pattern = r"(?=[+\-])"
        left_terms = re.split(pattern, polynomial_left)
        right_terms = re.split(pattern, polynomial_right)

        terms = []
        for term in left_terms:
            if not term:
                continue
            if term == "+" or term == "-":
                raise ValueError("Invalid polynomial string: invalid operator sequence.")
            terms.append(PolynomialTerm.from_string(term))

        for term in right_terms:
            if not term:
                continue
            new_term = PolynomialTerm.from_string(term)
            new_term.coefficient *= -1
            terms.append(new_term)

        return terms
