# Exercise 6 - First Unique Character Finder
# Return the index of the first character that appears only once in s, or -1.
# Two approaches: two passes with a dictionary, one pass with an ordered dictionary.


# 1 - TWO PASS
def first_unique_two_pass(s, n):
    frequency = {}

    # pass 1: count the occurrences of every character
    for i in range(n):
        if s[i] in frequency:
            frequency[s[i]] = frequency[s[i]] + 1
        else:
            frequency[s[i]] = 1

    # pass 2: return the first character whose count is exactly 1
    for i in range(n):
        if frequency[s[i]] == 1:
            return i
    return -1


# 2 - SINGLE PASS
def first_unique_ordered(s, n):
    # since Python 3.7 a normal dictionary keeps the insertion order of the keys,
    # so it works as the ordered dictionary of the pseudo-code
    first_index = {}

    # one pass: record the first index, mark a repeat with -1
    for i in range(n):
        if s[i] in first_index:
            first_index[s[i]] = -1
        else:
            first_index[s[i]] = i

    # the keys come back in insertion order, so the first surviving
    # index is already the leftmost unique character
    for key in first_index:
        if first_index[key] != -1:
            return first_index[key]
    return -1


def run_tests():
    # (input, expected result)
    tests = [
        # "c", "b", "o" and "n" appear once, the first of them is the "c" at the start
        ("carbonara", 0),
        # unique character in the middle (the "i")
        ("arrabbiata", 6),
        # no unique character, every letter appears two times or more
        ("carbonaracarbonara", -1),
        # unique character at the end
        ("carbonaracarbonara!", 18),
        # empty string
        ("", -1),
        # single character
        ("c", 0),
    ]

    for s, expected in tests:
        result1 = first_unique_two_pass(s, len(s))
        result2 = first_unique_ordered(s, len(s))
        if result1 == expected and result2 == expected:
            print("OK", '"' + s + '"', "->", result1)
        else:
            print("FAIL", '"' + s + '"', "->", result1, result2, "but expected", expected)


if __name__ == "__main__":
    run_tests()
