# Exercise 1 - Integer Mirror
# Reverse the decimal digits of a non-negative integer.
# Only arithmetic operations are used, no conversion to string.


def reverse_digits(n):
    # negative numbers are not accepted
    if n < 0:
        print("Error: n must be a non-negative integer")
        return -1

    mirror = 0
    while n > 0:
        # take the last digit
        digit = n % 10
        # add it to the end of the result
        mirror = mirror * 10 + digit
        # remove it from n
        n = n // 10
    return mirror


def run_tests():
    # (input, expected result)
    tests = [
        (315, 513),
        # trailing zeros
        (400, 4),
        # single digit
        (7, 7),
        (0, 0),
        # zeros in the middle
        (10203, 30201),
        # negative input, not accepted
        (-12, -1),
    ]

    for n, expected in tests:
        result = reverse_digits(n)
        if result == expected:
            print("OK", n, "->", result)
        else:
            print("FAIL", n, "->", result, "but expected", expected)


if __name__ == "__main__":
    run_tests()
