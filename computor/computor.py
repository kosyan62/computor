import argparse
from polynominal import PolynomParser, PolynomialFactory


def init_argparse():
    parser = argparse.ArgumentParser(
        prog="ft_computor_v1",
        description="program that solves a polynomial second or lower degree equation.",
    )
    parser.add_argument("equation", type=str, help="An equation to solve")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print additional information")
    return parser


def main():
    polynomial_factory = PolynomialFactory(PolynomParser())
    arg_parser = init_argparse()
    args = arg_parser.parse_args()
    try:
        polynomial = polynomial_factory.create(args.equation)
        if args.verbose:
            print("Reduced form: ", polynomial.get_reduced_form())
            print("Polynomial degree: ", polynomial.degree)
            if polynomial.degree == 2:
                print("Discriminant: ", polynomial.discriminant)
            print("Solutions count: ", polynomial.solutions_count)
        print("Solutions: ", polynomial.get_solution_string())
    except Exception as e:
        print("Error: " + str(e))


if __name__ == "__main__":
    main()
