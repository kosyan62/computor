from typing import List, Set, Iterable, Tuple

SMALLEST_PRIME = 2


def sqrt_str(x):
    is_complex = False
    if x < 0:
        is_complex = True
        x *= -1

    # Find the largest perfect square factor
    i = int(x ** 0.5)
    while i > 1:
        if x % (i * i) == 0:
            outside = str(i)
            inside = str(int(x // (i * i)))
            result = outside + "*sqrt(" + inside + ")" if inside != "1" else outside
            if is_complex:
                result += "*I"
            return result
        i -= 1

    # If no perfect square factors found, return the original format
    res = x ** 0.5
    if res % 1 != 0:
        res = "sqrt(" + str(x) + ")"
    else:
        res = str(int(res))
    if is_complex:
        res += "*I"
    return res


def get_prime_factors(number: int) -> Set[int]:
    """Recursively decompose a number into its prime factors."""
    # Base cases
    if number <= 1:
        return set()

    divisor = SMALLEST_PRIME
    while divisor * divisor <= number:
        if number % divisor == 0:
            return {divisor} | get_prime_factors(number // divisor)

        divisor += 1

    return {number}


def divide_str(x, y):
    """Divide two numbers and return the result as a string."""
    if isinstance(y, str):
        try:
            y = int(y)
        except ValueError:
            raise ValueError("y must be an integer to divide by")
    if y == 0:
        raise ValueError("Division by zero")
    if isinstance(x, str):
        # Here we want to extract a dividable part from x
        dividable_part = 1
        non_dividable_part = []
        if "*" in x:
            x_array = x.split("*")
            for multiplier in x_array:
                try:
                    dividable_part = int(multiplier)
                except ValueError:
                    non_dividable_part.append(multiplier)
        else:
            non_dividable_part.append(x)
        non_dividable_part = "*".join(non_dividable_part)
    else:
        dividable_part = x
        non_dividable_part = ""

    numerator, denominator = simplify_fraction(dividable_part, y)
    if numerator == 0:
        return "0"
    if non_dividable_part:
        if numerator == 1:
            result = non_dividable_part + "/" + str(denominator)
        else:
            result = str(numerator) + "*" + non_dividable_part + "/" + str(denominator)
    else:
        result = str(numerator) + "/" + str(denominator)

    if result.endswith("/1"):
        result = result[:-2]

    return result


def prod(factors: Iterable[int]):
    """Calculate the product of the iterable with integers."""
    result = 1
    for factor in factors:
        result *= factor
    return result


def simplify_fraction(x, y) -> Tuple[int, int]:
    """Simplify a fraction x/y into its simplest form. Returns a tuple (numerator, denominator)."""
    if y == 0:
        raise ZeroDivisionError("Division by zero")
    if x == 0:
        return 0, 1
    if x % y == 0:
        return x // y, 1
    sign = -1 if x / y < 0 else 1
    x, y = abs(x), abs(y)
    x_primes = get_prime_factors(x)
    y_primes = get_prime_factors(y)
    common_primes = set.intersection(x_primes, y_primes)
    common_multiplier = 1
    for prime in common_primes:
        x_reduced = x
        y_reduced = y
        while x_reduced % prime == 0 and y_reduced % prime == 0:
            common_multiplier *= prime
            x_reduced //= prime
            y_reduced //= prime
    x, y = x // common_multiplier, y // common_multiplier
    return sign * x, y
