import pandas as pd

from polynominal import PolynomialTerm


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
df = pd.read_csv("quadratic_equations_dataset_with_solutions.csv", header=0)

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

df = pd.read_csv("quadratic_equations_dataset_with_solutions.csv", header=0)
# take first ten lines
# df = df.head(20)

data_polynom_second_degree_all_positive_tuple = []
for index, row in df.iterrows():
    data_polynom_second_degree_all_positive_tuple.append(
        (row["Equation"], row["Discriminant"], row["Roots"])
    )
# data_polynom_second_degree_all_positive_tuple = [
#     ("5x^2 + 0x + 4 = 0", -80, "x = -2*sqrt(5)*I/5, x = 2*sqrt(5)*I/5",)
#
# ]

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
]

data_polynom_first_degree_negative_tuple = [
    ("0 * X = 0", float("inf")),
    ("0 * X = 1", 0),
]
