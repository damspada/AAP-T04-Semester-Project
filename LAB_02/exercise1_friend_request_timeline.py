# Exercise 1 - Friend Request Timeline
# Analyze a friend request message with its characters: uppercase letters,
# urgency punctuation, caps ratio, label and letters repeated more than 3 times.
# The character comparisons are counted while the message is read.


# number of character comparisons done by the last call of analyze_request
comparisons = 0


def is_letter(c):
    global comparisons
    comparisons = comparisons + 1
    return c.isalpha()


def is_uppercase(c):
    global comparisons
    comparisons = comparisons + 1
    return c.isupper()


def compare(a, b):
    global comparisons
    comparisons = comparisons + 1
    return a == b


def analyze_request(msg):
    global comparisons
    comparisons = 0

    upper = 0
    alpha = 0
    punct = 0
    run = 0
    max_run = 0
    # no previous letter yet
    prev = ""

    for c in msg:
        if is_letter(c):
            # count the letters and the uppercase letters
            alpha = alpha + 1
            if is_uppercase(c):
                upper = upper + 1
            # length of the current run of equal letters, like "yyyy" in "heyyyy"
            if compare(c.lower(), prev):
                run = run + 1
            else:
                run = 1
                prev = c.lower()
            if run > max_run:
                max_run = run
        else:
            # only letters make a run: "!!!!" is already counted as punctuation
            run = 0
            prev = ""
            # count the urgency punctuation
            # "or" stops at the first true comparison, so only the comparisons really done are counted
            if compare(c, "!") or compare(c, "?"):
                punct = punct + 1

    # avoid the division by zero when there are no letters
    if alpha > 0:
        caps_ratio = upper / alpha
    else:
        caps_ratio = 0

    # from the strongest to the weakest condition
    if caps_ratio >= 0.6 or punct >= 5:
        label = "AGGRESSIVE"
    elif caps_ratio >= 0.3 or punct >= 3:
        label = "URGENT"
    else:
        label = "CALM"

    # more than 3 equal letters in a row
    spam = max_run > 3
    return upper, punct, caps_ratio, label, spam


def run_tests():
    # (message, expected upper, punct, caps ratio, label, spam)
    tests = [
        # the three examples of the lab (the caps ratio is computed on the letters only)
        ("Hey, want to connect?", 1, 1, 1 / 16, "CALM", False),
        ("PLEASE ACCEPT MY REQUEST!!!", 21, 3, 1.0, "AGGRESSIVE", False),
        ("Are you free? I need to talk!!!", 2, 4, 2 / 21, "URGENT", False),
        # empty message
        ("", 0, 0, 0, "CALM", False),
        # no letters, so no division by zero
        ("?!?!?", 0, 5, 0, "AGGRESSIVE", False),
        # caps ratio exactly 0.3
        ("PIZza buona", 3, 0, 0.3, "URGENT", False),
        # caps ratio exactly 0.6
        ("FORza", 3, 0, 0.6, "AGGRESSIVE", False),
        # short message with an accent: the ratio is 1 even if the message does not shout
        ("SÌ", 2, 0, 1.0, "AGGRESSIVE", False),
        # repeated letters
        ("ciaooooo", 0, 0, 0, "CALM", True),
        # only 3 equal letters in a row, not spam
        ("grazieee", 0, 0, 0, "CALM", False),
        # uppercase and lowercase are the same letter in a run
        ("BelliSSSsimo", 4, 0, 4 / 12, "URGENT", True),
        # a space breaks the run
        ("Daiii iii", 1, 0, 1 / 8, "CALM", False),
        # spam and urgent together
        ("Carbonaraaaa!!!", 1, 3, 1 / 12, "URGENT", True),
        # letters with accents
        ("PERCHÉ?", 6, 1, 1.0, "AGGRESSIVE", False),
    ]

    for msg, upper, punct, ratio, label, spam in tests:
        result = analyze_request(msg)
        # floats are not always exact, so we accept a very small difference for the ratio
        if (result[0] == upper and result[1] == punct and abs(result[2] - ratio) < 1e-9
                and result[3] == label and result[4] == spam):
            print("OK", '"' + msg + '"', "->", result[0], result[1], round(result[2], 2),
                  result[3], result[4], "comparisons:", comparisons)
        else:
            print("FAIL", '"' + msg + '"', "->", result, "but expected", (upper, punct, ratio, label, spam))


if __name__ == "__main__":
    run_tests()
