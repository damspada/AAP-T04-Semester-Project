# Exercise 2 - Balanced Symbol Checker
# Check if a string of ( ) [ ] { } is balanced, using a stack.
# The number of comparisons is counted while the string is checked.


# number of comparisons done by the last call of is_balanced
comparisons = 0


def compare(a, b):
    global comparisons
    comparisons = comparisons + 1
    return a == b


def is_balanced(s):
    global comparisons
    comparisons = 0

    # a Python list is used as a stack: append = push, pop = pop
    stack = []
    for char in s:
        # the three opening symbols are pushed and wait for their closer
        # "or" stops at the first true comparison, so only the comparisons really done are counted
        if compare(char, "(") or compare(char, "[") or compare(char, "{"):
            stack.append(char)

        # a closer needs its own opener on top of the stack
        elif compare(char, ")"):
            if compare(len(stack), 0):
                return False
            top = stack.pop()
            if not compare(top, "("):
                return False

        elif compare(char, "]"):
            if compare(len(stack), 0):
                return False
            top = stack.pop()
            if not compare(top, "["):
                return False

        elif compare(char, "}"):
            if compare(len(stack), 0):
                return False
            top = stack.pop()
            if not compare(top, "{"):
                return False

    # a leftover opener means the string is unclosed
    return compare(len(stack), 0)


def run_tests():
    # (input, expected result)
    tests = [
        ("({[]})", True),
        # wrong nesting
        ("([)]", False),
        # empty string
        ("", True),
        # missing closer
        ("((())", False),
        # closer before opener
        (")(", False),
        # other characters are ignored
        ("if (a[i] > 0) { x = f(y); }", True),
    ]

    for s, expected in tests:
        result = is_balanced(s)
        if result == expected:
            print("OK", '"' + s + '"', "->", result, "comparisons:", comparisons)
        else:
            print("FAIL", '"' + s + '"', "->", result, "but expected", expected)


if __name__ == "__main__":
    run_tests()
