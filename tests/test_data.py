import pandas as pd

from computor.polynominal import PolynomialTerm


def transform_roots(roots):
    roots = roots.split(",")
    new_roots = set()
    for root in roots:
        root = root.replace(" ", "")
        root = root.replace("x=", "")
        if "/" in root:
            root = root.split("/")
            new_roots.add(float(root[0]) / float(root[1]))
        else:
            new_roots.add(float(root))
    return new_roots


# Originally dataset from https://huggingface.co/datasets/Jack010/QuadraticDataset
csv_path = __file__.replace("test_data.py", "quadratic_equations_dataset_with_solutions.csv")
df = pd.read_csv(csv_path, header=0)

# find all with 'Real and distinct'
df = df[df["Root Type"] == "Real and Distinct"]
df = df[~df["Roots"].str.contains("sqrt")]

# Prepare test data from dataset
data_polynom_second_degree_positive_tuple = []
ids_polynom_second_degree_positive = []
for index, row in df.iterrows():
    data_polynom_second_degree_positive_tuple.append(
        (row["Equation"], row["Discriminant"], transform_roots(row["Roots"]))
    )
    ids_polynom_second_degree_positive.append(
        f"Equasion {row['Equation']} with roots {row['Roots']} "
    )

df = pd.read_csv(csv_path, header=0)

data_polynom_second_degree_all_positive_tuple = []
for index, row in df.iterrows():
    data_polynom_second_degree_all_positive_tuple.append(
        (row["Equation"], row["Discriminant"], row["Roots"])
    )

data_polynom_term_positive_tuple = [
    # Zero cases
    ("0", PolynomialTerm(0, 0)),
    ("-0", PolynomialTerm(0, 0)),
    ("+0", PolynomialTerm(0, 0)),
    # Simple variable X cases
    ("X", PolynomialTerm(1, 1)),
    ("+X", PolynomialTerm(1, 1)),
    ("-X", PolynomialTerm(-1, 1)),
    ("0X", PolynomialTerm(0, 1)),
    ("0*X", PolynomialTerm(0, 1)),
    # Simple number cases
    ("4", PolynomialTerm(4, 0)),
    ("+4", PolynomialTerm(4, 0)),
    ("-4", PolynomialTerm(-4, 0)),
    # Power cases with coefficient 1
    ("X^2", PolynomialTerm(1, 2)),
    ("-X^2", PolynomialTerm(-1, 2)),
    ("+X^2", PolynomialTerm(1, 2)),
    ("X^3", PolynomialTerm(1, 3)),
    ("X^4", PolynomialTerm(1, 4)),
    # Coefficient * Variable cases
    ("2*X", PolynomialTerm(2, 1)),
    ("-2*X", PolynomialTerm(-2, 1)),
    ("+2*X", PolynomialTerm(2, 1)),
    ("X*2", PolynomialTerm(2, 1)),
    ("2X", PolynomialTerm(2, 1)),
    # Coefficient * Variable^Power cases
    ("2*X^2", PolynomialTerm(2, 2)),
    ("-2*X^2", PolynomialTerm(-2, 2)),
    ("+2*X^2", PolynomialTerm(2, 2)),
    ("3*X^4", PolynomialTerm(3, 4)),
    ("-3*X^4", PolynomialTerm(-3, 4)),
    ("X^2*2", PolynomialTerm(2, 2)),
    ("2X^2", PolynomialTerm(2, 2)),
    ("123X^2", PolynomialTerm(123, 2)),
    ("X^2*123", PolynomialTerm(123, 2)),
    # Edge cases with spaces (should be handled by normalization)
    (" 2 * X ^ 2 ", PolynomialTerm(2, 2)),
    ("2* X^2", PolynomialTerm(2, 2)),
    ("2 *X^2", PolynomialTerm(2, 2)),
    # More variations of zero
    ("00", PolynomialTerm(0, 0)),
    ("00*X", PolynomialTerm(0, 1)),
    ("00*X^0", PolynomialTerm(0, 0)),
    # Large numbers
    ("1000*X", PolynomialTerm(1000, 1)),
    ("1000", PolynomialTerm(1000, 0)),
    ("-1000*X^2", PolynomialTerm(-1000, 2)),
    # Higher powers
    ("X^10", PolynomialTerm(1, 10)),
    ("-X^10", PolynomialTerm(-1, 10)),
    ("2*X^10", PolynomialTerm(2, 10)),
    # Alternative positions of multiplication
    ("X*2", PolynomialTerm(2, 1)),
    ("X*-2", PolynomialTerm(-2, 1)),
    # Different forms of the same term
    ("X^1", PolynomialTerm(1, 1)),
    ("1*X^1", PolynomialTerm(1, 1)),
    ("+1*X^1", PolynomialTerm(1, 1)),
    # Mixed signs with zeros
    ("+0*X^0", PolynomialTerm(0, 0)),
    ("-0*X^1", PolynomialTerm(0, 1)),
    # Boundary values
    ("2147483647*X", PolynomialTerm(2147483647, 1)),  # Max int
    ("-2147483648*X", PolynomialTerm(-2147483648, 1)),  # Min int
    # Multiple zeros in coefficient
    ("01*X", PolynomialTerm(1, 1)),
    ("001*X", PolynomialTerm(1, 1)),
    # Zero power with different coefficients
    ("42*X^0", PolynomialTerm(42, 0)),
    ("-42*X^0", PolynomialTerm(-42, 0)),
]

data_polynom_parser_positive_string = [
    {"input": "0=0", "expected": [PolynomialTerm(0, 0), PolynomialTerm(0, 0)]},
    {"input": "X=0", "expected": [PolynomialTerm(1, 1), PolynomialTerm(0, 0)]},
    {"input": "X^2=0", "expected": [PolynomialTerm(1, 2), PolynomialTerm(0, 0)]},
    {
        "input": "X^2+X=0",
        "expected": [PolynomialTerm(1, 2), PolynomialTerm(1, 1), PolynomialTerm(0, 0)],
    },
    {
        "input": "-X^2=0",
        "expected": [PolynomialTerm(-1, 2), PolynomialTerm(0, 0)]},
    {
        "input": "X^2+X^3=0",
        "expected": [PolynomialTerm(1, 2), PolynomialTerm(1, 3), PolynomialTerm(0, 0)],
    },
    {
        "input": "X^2+X^3+X=-1",
        "expected": [
            PolynomialTerm(1, 2),
            PolynomialTerm(1, 3),
            PolynomialTerm(1, 1),
            PolynomialTerm(1, 0),
        ],
    },
    {
        "input": "2*X^2+3*X^3+4*X^4-1=0",
        "expected": [
            PolynomialTerm(2, 2),
            PolynomialTerm(3, 3),
            PolynomialTerm(4, 4),
            PolynomialTerm(-1, 0),
            PolynomialTerm(0, 0),
        ],
    },  # String with spaces. Normalization test
    {
        "input": "  2 *X ^ 2+ 3* X ^3+ 4 * x ^ 4 -1 = 0  ",
        "expected": [
            PolynomialTerm(2, 2),
            PolynomialTerm(3, 3),
            PolynomialTerm(4, 4),
            PolynomialTerm(-1, 0),
            PolynomialTerm(0, 0),
        ],
    },
]
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
    {"input": "*X*2=0", "expected": "Invalid term"},
    {"input": "2**X=0", "expected": "Invalid term"},
    {"input": "X**2=0", "expected": "Invalid term"},
    {"input": "2*X**2=0", "expected": "Invalid term"},
    {"input": "X^2^2=0", "expected": "Invalid term"},
    {"input": "=", "expected": "Invalid polynomial string"},
    {"input": "==", "expected": "Invalid polynomial string"},
    {"input": " = ", "expected": "Invalid polynomial string"},
    {"input": "X = 1*2", "expected": "Invalid term"},

    # No '=' at all
    {"input": "X^2+3*X", "expected": "Invalid polynomial string"},
    {"input": "3*X^2+X^1-1", "expected": "Invalid polynomial string"},

    # Multiple '=' signs
    {"input": "X=3=X", "expected": "Invalid polynomial string"},
    {"input": "0=X=0", "expected": "Invalid polynomial string"},

    # Empty sides
    {"input": "= ", "expected": "Invalid polynomial string"},
    {"input": " =0", "expected": "Invalid polynomial string"},
    {"input": "X^2 + 3*X= ", "expected": "Invalid polynomial string"},

    # Garbled syntax
    {"input": "X^2++3*X=0", "expected": "Invalid polynomial string"},
    {"input": "X^2--3*X=0", "expected": "Invalid polynomial string"},
    {"input": "X^2+-3*X=0", "expected": "Invalid polynomial string"},
    {"input": "+-3*X^2=0", "expected": "Invalid polynomial string"},
    {"input": "--3*X^2=0", "expected": "Invalid polynomial string"},
    {"input": "**3*X^2=0", "expected": "Invalid term"},

    # Misplaced operators
    {"input": "X^+2=0", "expected": "Invalid polynomial string"},
    {"input": "X^-=0", "expected": "Invalid polynomial string"},
    {"input": "X^--2=0", "expected": "Invalid polynomial string"},
    {"input": "X^=2", "expected": "Invalid polynomial string"},
    {"input": "3^X=0", "expected": "Invalid polynomial string"},
    {"input": "*X=0", "expected": "Invalid term"},
    {"input": "X*=2", "expected": "Invalid term"},
    {"input": "X^2*=0", "expected": "Invalid term"},
    {"input": "X^2=*", "expected": "Invalid term"},
    {"input": "X^*2=0", "expected": "Invalid polynomial string"},
    {"input": "X^^2=0", "expected": "Invalid polynomial string"},
    {"input": "3*X^^2=0", "expected": "Invalid polynomial string"},

    # Symbols used incorrectly
    {"input": "X/2=0", "expected": "Invalid polynomial string"},
    {"input": "X@2=0", "expected": "Invalid polynomial string"},
    {"input": "2&X=0", "expected": "Invalid polynomial string"},
    {"input": "X#2=0", "expected": "Invalid polynomial string"},

    # Mixed identifiers
    {"input": "2*Y^2=0", "expected": "Invalid polynomial string"},
    {"input": "x*y=0", "expected": "Invalid polynomial string"},
    {"input": "3*X^a=0", "expected": "Invalid polynomial string"},
    {"input": "X^2.5=0", "expected": "Invalid polynomial string"},

    # Typos and misplaced expressions
    {"input": "X^^=0", "expected": "Invalid polynomial string"},
    {"input": "X^^^2=0", "expected": "Invalid polynomial string"},
    {"input": "3*X^2+=0", "expected": "Invalid polynomial string"},
    {"input": "3**X=0", "expected": "Invalid term"},
    {"input": "X^2++", "expected": "Invalid polynomial string"},
    {"input": "3*X^^=0", "expected": "Invalid polynomial string"},

    # Leading or trailing operator
    {"input": "+=X^2", "expected": "Invalid polynomial string"},
    {"input": "-=X", "expected": "Invalid polynomial string"},
    {"input": "+=+3*X^2", "expected": "Invalid polynomial string"},

    # Ambiguous compound terms
    {"input": "2X3X=0", "expected": "Invalid term"},
    {"input": "X2X=0", "expected": "Invalid term"},

]

data_polynom_second_degree_reduce_positive_string = [
    {"input": "X^2+X-0=0", "expected": "1 * X^2 + 1 * X^1 + 0 * X^0 = 0"},
    {"input": "X^2+X-X+X-X+X-1=0", "expected": "1 * X^2 + 1 * X^1 - 1 * X^0 = 0"},
    {
        "input": "32X^2+32X-32=31X^2+31X-31",
        "expected": "1 * X^2 + 1 * X^1 - 1 * X^0 = 0",
    },
]

data_polynom_first_degree_positive_tuple = [
    ("2x - 6 = 0", 3),
    ("x = 2", 2),
    ("2 * X - 32 = 64", 48),
    ("x = 0", 0),
    ("0 = X", 0),
    ("- X = 0", 0),
    ("x - x + x - X = X", 0),

    # Additional test cases:
    ("3*x = 12", 4),                        # simple division
    ("3x - x = 4", 2),                      # reduction needed
    ("x + 3 = 7", 4),                       # isolate x
    ("7 = x + 3", 4),                       # inverse side
    ("x - 4 = 2", 6),                       # add to both sides
    ("-x = 4", -4),                         # negative x
    ("-2x + 8 = 0", 4),                     # isolate and divide
    ("5*x + 3 = 3", 0),                     # constant cancels
    ("-x = -1", 1),                         # double negative
    ("3*X + 9 = 3", -2),                    # negative result
    ("X + X + X = 9", 3),                   # multiple same terms
    ("0 = 2x - 10", 5),                     # RHS zero
    ("0 = -3x + 9", 3),                     # negative coeff
    ("10 = 2*x + 4", 3),                    # normal form
    ("   x=2   ", 2),                       # whitespace
    ("X - 0 = 0", 0),                       # trivial
    ("0 = 0 + X", 0),                       # identity
    ("x = 2", 2),  # already in solved form
    ("x = -3", -3),  # negative RHS
    ("x = 0", 0),  # zero RHS
    ("x + 1 = 5", 4),  # move RHS
    ("5 = x + 1", 4),  # flipped sides
    ("-x = -3", 3),  # simple negation
    ("x - 2 = 5", 7),  # isolate x
    ("3 = x - 1", 4),  # inverse again
    ("2x = x + 4", 4),  # requires reduction
    ("x + x = 2", 1),  # combine like terms
]

data_polynom_first_degree_negative_tuple = [
    ("0 * X = 0", float("inf")),
    ("0 * X = 1", 0),
    ("2x = x + x", float("inf")),  # identity form
    ("x = x", float("inf")),  # identity
    ("x = x + 1", -1),  # contradiction
    ("2x + 1 = 2x + 1", float("inf")),  # identity with terms
    ("2x + 1 = 2x - 1", -1),  # contradiction
]
