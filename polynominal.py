import re
from abc import ABC, abstractmethod
from typing import List, Tuple

from utils import sqrt_str, divide_str


class PolynomialTerm:
    def __init__(self, coefficient, degree):
        self.coefficient = coefficient
        self.degree = degree

    def copy(self):
        return PolynomialTerm(self.coefficient, self.degree)

    @classmethod
    def from_string(cls, term_str: str) -> "PolynomialTerm":
        """Create a PolynomialTerm from a string representation.

        Args:
            term_str: String representation of polynomial term (e.g., "2X^3", "X", "-5X^2")

        Returns:
            PolynomialTerm instance

        Raises:
            ValueError: If the input string format is invalid
        """
        # Normalize input
        try:
            term_str = cls._normalize_input(term_str)
        except ValueError as e:
            raise ValueError(f'Invalid term - "{term_str}": {e}') from e

        # Parse coefficient and degree
        coefficient, degree = cls._parse_term(term_str)

        return cls(coefficient, degree)

    @staticmethod
    def _normalize_input(term_str: str) -> str:
        """Normalize the input string by adding implicit parts."""

        if not isinstance(term_str, str):
            raise ValueError("Input must be a string")

        term_str = term_str.replace(" ", "")

        # Check string for valid symbols
        allowed_symbols = set("+-*^X0123456789")
        if not set(term_str).issubset(allowed_symbols):
            raise ValueError("Contains invalid characters")

        if term_str == "" or term_str == "+" or term_str == "-":
            raise ValueError("Term cannot be empty or only contain + or -")

        if term_str == "X" or term_str == "+X":
            return "1*X^1"
        elif term_str == "-X":
            return "-1*X^1"
        if "X" not in term_str:
            # Add implicit X^0 for constant terms
            term_str = f"{term_str}*X^0"
        elif term_str.count("X") > 1:
            raise ValueError("Contains multiple X")
        if term_str.count("*") > 1:
            raise ValueError("Contains multiple *")
        if term_str.startswith("*") or term_str.endswith("*"):
            raise ValueError("Contains invalid start or end *")
        if term_str.count("^") > 1:
            raise ValueError("Contains multiple ^")
        x_pos = term_str.index("X")
        if not term_str.endswith("X") and term_str[x_pos + 1] not in ("*", "^"):
            raise ValueError("X must be followed by * or ^")
        if not term_str.startswith("X"):
            x_start = x_pos - 1
            if term_str[x_start] == "-":
                term_str = term_str[:x_start] + "-1*" + term_str[x_start + 1 :]
            elif term_str[x_start] == "+":
                term_str = term_str[:x_start] + "+1*" + term_str[x_start + 1 :]
            elif term_str[x_start].isdigit():
                term_str = term_str[: x_start + 1] + "*" + term_str[x_start + 1 :]
            elif term_str[x_start] != "*":
                raise ValueError("X must be preceded by +, -, * or a digit")
        if any(
            [b in term_str for b in ("--", "++", "+-", "-+", "-*", "+*", "*^", "^*")]
        ):
            raise ValueError("Contains invalid operator sequence")
        if "X" in term_str and "X^" not in term_str:
            term_str = term_str.replace("X", "X^1")

        return term_str

    @staticmethod
    def _parse_term(term_str: str) -> tuple[int, int]:
        """Parse coefficient and degree from normalized term string."""

        if "*" not in term_str:
            if "X" in term_str:
                term_str = "1*" + term_str
            else:
                term_str = term_str * "X^0"
        left, right = term_str.split("*")
        coefficient, degree = (left, right) if "X" in right else (right, left)
        if not coefficient:
            coefficient = 1
        elif coefficient == "-":
            coefficient = -1

        return int(coefficient), int(degree.replace("X^", ""))

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

    @property
    @abstractmethod
    def solutions_count(self) -> int:
        """Returns the number of solutions for the polynomial."""
        raise NotImplementedError

    @abstractmethod
    def get_solutions(self) -> Tuple[float]:
        """Returns the solutions for the polynomial."""
        raise NotImplementedError

    @abstractmethod
    def get_solution_string(self) -> str:
        """Returns a string representation of the solutions."""
        raise NotImplementedError

    @property
    def degree(self) -> int:
        """Returns the degree of the polynomial."""
        if self._degree is None:
            self._degree = self.find_max_degree(self.terms)
        return self._degree

    @property
    def terms(self) -> List[PolynomialTerm]:
        return self._terms

    @terms.setter
    def terms(self, terms: List[PolynomialTerm]):
        if self._terms is not None:
            raise ValueError("Terms cannot be set after initialization.")
        self._terms = self.reduce_terms(terms)

    def get_reduced_form(self) -> str:
        """Returns the reduced form of the polynomial."""
        reduced_form = ""

        if not self.terms:
            return "0 * X^0 = 0"
        for term in reversed(self.terms):
            term_str = str(term)
            if term.coefficient >= 0:
                term_str = "+" + term_str
            reduced_form += f"{term_str}"

        if reduced_form[0] == "+":
            reduced_form = reduced_form[1:]

        reduced_form = reduced_form.replace("*", " * ")
        reduced_form = reduced_form.replace("=", " = ")
        reduced_form = reduced_form.replace("-", " - ")
        reduced_form = reduced_form.replace("+", " + ")

        return reduced_form + " = 0"

    @staticmethod
    def reduce_terms(terms: List[PolynomialTerm]) -> List[PolynomialTerm]:
        """
        Sets the terms of the polynomial while reducing terms to the same degree by
        combining their coefficients.

        This setter method processes the list of polynomial terms and consolidates duplicate
        terms by degree, ensuring that each degree has a single term with a summed coefficient.

        :param terms: A list of polynomial terms to be set in the polynomial. Each term
            is an instance of the PolynomialTerm class and contains a degree and
            coefficient.
        :type terms: List[PolynomialTerm]
        :return: None
        """
        if not isinstance(terms, list):
            raise ValueError("Value of terms must be a list of PolynomialTerm objects.")
        reduced_terms = {}
        for term in terms:
            if not isinstance(term, PolynomialTerm):
                raise ValueError(
                    "Value of terms must be a list of PolynomialTerm objects."
                )
            if term.degree not in reduced_terms.keys():
                reduced_terms[term.degree] = term.copy()
            else:
                reduced_terms[term.degree].coefficient += term.coefficient
                # We're reducing on the go here
                if reduced_terms[term.degree].coefficient == 0:
                    del reduced_terms[term.degree]

        if not reduced_terms:
            return []
        # if a term is missing, we're adding it with a 0 coefficient
        for degree in range(max(reduced_terms.keys()) + 1):
            if degree not in reduced_terms:
                reduced_terms[degree] = PolynomialTerm(0, degree)

        return sorted(reduced_terms.values(), key=lambda x: x.degree)

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
            0: PolynomialZeroDegree,
            1: PolynomialFirstDegree,
            2: PolynomialSecondDegree,
        }

    def create(self, polynom_str):
        """Create a polynomial object based on the polynomial string."""
        polynom_terms = self.parser.parse(polynom_str)
        reduced_terms = Polynomial.reduce_terms(polynom_terms)
        degree = Polynomial.find_max_degree(reduced_terms)
        if degree not in self.polynomials.keys():
            raise ValueError(f"Polynomial of degree {degree} is not supported.")
        return self.polynomials[degree](polynom_terms)


class PolynomialZeroDegree(Polynomial):
    """Represents a zero degree polynomial."""

    def get_solutions(self) -> Tuple[float]:
        return ()

    def get_solution_string(self) -> str:
        if self.solutions_count == -1:
            return "The sides of equation are not equal. Cannot solve."
        else:
            return "Any X is solution"

    @property
    def solutions_count(self) -> int:
        if self.terms:
            return -1
        else:
            return float("inf")

    def __init__(self, terms):
        super().__init__(terms)


class PolynomialFirstDegree(Polynomial):
    """Represents a first degree polynomial."""

    @property
    def a(self):
        return self.terms[-1].coefficient

    @property
    def b(self):
        return self.terms[-2].coefficient

    def get_solutions(self) -> Tuple[float]:
        if self.solutions_count != 1:
            return tuple()
        return (-1 * self.b / self.a,)

    def get_solution_string(self) -> str:
        if self.solutions_count == 0:
            return "No solutions"
        elif self.solutions_count == float("inf"):
            return "Any x is solution"
        else:
            return "x = " + divide_str(self.b, self.a)

    @property
    def solutions_count(self) -> int:
        if self.a == 0:
            if self.b == 0:
                return float("inf")
            else:
                return 0
        return 1

    def __init__(self, terms):
        super().__init__(terms)


class PolynomialSecondDegree(Polynomial):
    @property
    def solutions_count(self) -> int:
        if self.discriminant == 0:
            return 1
        else:
            return 2

    @property
    def discriminant(self):
        if self._discriminant is None:
            self._discriminant = self.b**2 - 4 * self.a * self.c
        return self._discriminant

    @property
    def a(self):
        return self.terms[-1].coefficient

    @property
    def b(self):
        return self.terms[-2].coefficient

    @property
    def c(self):
        return self.terms[-3].coefficient

    def __init__(self, terms):
        super().__init__(terms)
        self._discriminant = None

    def get_solutions(self) -> Tuple[float]:
        if self.discriminant != 0:
            x1 = (-self.b + self.discriminant**0.5) / (2 * self.a)
            x2 = (-self.b - self.discriminant**0.5) / (2 * self.a)
            return x1, x2
        else:
            return (-self.b / (2 * self.a),)

    def get_solution_string(self) -> str:
        if self.discriminant == 0:
            return "x = " + divide_str(-self.b, 2 * self.a)
        else:
            discriminant_sqrt = sqrt_str(self.discriminant)
            try:
                discriminant_sqrt = int(discriminant_sqrt)
                x1 = divide_str(-self.b + discriminant_sqrt, 2 * self.a)
                x2 = divide_str(-self.b - discriminant_sqrt, 2 * self.a)
            except ValueError:
                left, right = divide_str(-self.b, 2 * self.a), divide_str(
                    discriminant_sqrt, 2 * self.a
                )
                if left == "0":
                    x1 = right
                    x2 = "-" + right
                else:
                    x1 = left + " + " + right
                    x2 = left + " - " + right
            return f"x = {x1}, x = {x2}"


class PolynomParser:
    pattern = r"^[\dX\^\-\+\*=]+$"  # Regex pattern to match a polynomial string

    @classmethod
    def normalize(cls, polynom_str: str):
        """Normalize and validate a polynomial string."""
        if not isinstance(polynom_str, str):
            raise ValueError("Invalid polynomial string to parse: not a string.")
        polynom_str = polynom_str.strip()
        polynom_str = polynom_str.replace("\n", "")
        polynom_str = polynom_str.replace("\t", "")
        polynom_str = polynom_str.replace(" ", "")
        polynom_str = polynom_str.replace("x", "X")
        polynom_str = polynom_str.replace("²", "^2")
        if re.match(cls.pattern, polynom_str) is None:
            raise ValueError(
                "Invalid polynomial string to parse: contains invalid characters."
            )
        if polynom_str.count("=") != 1:
            raise ValueError(
                "Invalid polynomial string to parse: '=' should be present exactly once."
            )
        if polynom_str.startswith("=") or polynom_str.endswith("="):
            raise ValueError(
                "Invalid polynomial string to parse: '=' should not be at the beginning or end."
            )
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
                raise ValueError(
                    "Invalid polynomial string: invalid operator sequence."
                )
            terms.append(PolynomialTerm.from_string(term))

        for term in right_terms:
            if not term:
                continue
            new_term = PolynomialTerm.from_string(term)
            new_term.coefficient *= -1
            terms.append(new_term)

        return terms
