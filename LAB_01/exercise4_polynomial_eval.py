# Exercise 4 - Polynomial Evaluation
# c[i] is the coefficient of x^i and n is the degree (so c has n + 1 values).


def horner_eval(c, n, x):
    result = 0
    # walk from the highest-degree coefficient down to the constant term
    for i in range(n, -1, -1):
        result = result * x + c[i]
    return result


def evaluate(coeffs, x):
    return horner_eval(coeffs, len(coeffs) - 1, x)


def run_tests():
    # (coefficients, x, expected result)
    tests = [
        ([3, -2, 0, 5], 2.0, 39.0),
        # constant polynomial
        ([7], 100.0, 7.0),
        # empty list, zero polynomial
        ([], 5.0, 0),
        # x = 0 gives c[0]
        ([4, 9, 9, 9], 0.0, 4.0),
        # result is 0.7000000000000001
        ([0.1, 0.2], 3.0, 0.7),
        # big integer, exact in Python
        ([1, 0, 1], 10**8, 10**16 + 1),
    ]

    for coeffs, x, expected in tests:
        result = evaluate(coeffs, x)
        # floats are not always exact, so we accept a very small difference
        if abs(result - expected) < 1e-9:
            print("OK", coeffs, "x =", x, "->", result)
        else:
            print("FAIL", coeffs, "x =", x, "->", result, "but expected", expected)


def precision_example():
    # with integers Python is exact, with floats the "+ 1" is lost (only about 16 digits)
    print("\nP(x) = 1 + x^2 at x = 10^8")
    print("with integers:", evaluate([1, 0, 1], 10**8))
    print("with floats:", evaluate([1.0, 0.0, 1.0], 1e8))


if __name__ == "__main__":
    run_tests()
    precision_example()
