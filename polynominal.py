import re

class PolynomSecondDegree:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self._discriminant = None

    @property
    def discriminant(self):
        if not self._discriminant:
            self._discriminant = self.b ** 2 - 4 * self.a * self.c


    def sulutions_count(self):
        if self.discriminant > 0:
            return 2
        elif self.discriminant == 0:
            return 1
        else:
            return 0


class PolynomTerm:
    def __init__(self, coefficient, degree):
        self.coefficient = coefficient
        self.degree = degree

    @classmethod
    def from_string(cls, term_str):
        """Create a PolynomTerm from a string representation."""
        pattern = r"^(?P<sign>[\-+])?(?P<coefficient>\d*)?(?P<x_part>X(\^(?P<degree>\d+))?)?$"
        match = re.match(pattern, term_str)
        if not match:
            raise ValueError(f"Invalid term string: {term_str}")
        sign = match.group("sign")
        coefficient = match.group("coefficient")
        x_part = match.group("x_part")
        degree = match.group("degree")
        if sign == '-':
            if coefficient is None or coefficient == '':
                coefficient = -1
            else:
                coefficient = -int(coefficient)
        else:
            if coefficient is None or coefficient == '':
                coefficient = 1
            else:
                coefficient = int(coefficient)
        if x_part is None:
            degree = 0
        elif degree is None:
            degree = 1
        else:
            degree = int(degree)
        return cls(coefficient, degree)

        


class PolynomParser:
    pattern = r"^[\dX^\-+*]+=[\dX^+\-*]+$" # Regex pattern to match a polynomial string

    def __init__(self, polynom_str):
        """Initialize the parser with a polynomial string."""
        normalized_str = self.normalize(polynom_str)
        self.polynom_str = self.parse(normalized_str)

    def normalize(self):
        """Normalize the polynomial string by removing spaces and ensuring it matches the expected format."""
        if not isinstance(self.polynom_str, str):
            raise ValueError("Invalid polynomial string to parse: not a string.")
        polynom_str = polynom_str.strip()
        polynom_str = polynom_str.replace(" ", "")
        polynom_str = polynom_str.replace("x", "X")
        if re.match(self.pattern, polynom_str) is None:
            raise ValueError("Invalid polynomial string to parse: contains invalid characters.")
        return polynom_str


    def parse(self):
        """Parse the polynomial string into list of terms."""
        # Split the polynomial string into parts based on operators
        pattern = r"(?=[=+\-])"
        parts = self.polynom_str.split(pattern)

        terms = []
        for part in parts:
            if part:
                terms.append(PolynomTerm.from_string(part))

            
        



        
    