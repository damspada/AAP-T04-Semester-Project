# Exercise 2 - Mutual Friends Detection Using Sets
# The friend lists are hash sets (Python set): "in" and add cost O(1) on average,
# and add ignores an element that is already in the set.
# Intersection, difference and union are written with loops, without the operators & - | of Python.


def intersection(a, b):
    r = set()
    # walk the smaller set and look for its elements in the bigger one
    if len(a) > len(b):
        # swap
        temp = a
        a = b
        b = temp
    for x in a:
        if x in b:
            r.add(x)
    return r


def difference(a, b):
    r = set()
    for x in a:
        if x not in b:
            r.add(x)
    return r


def union(a, b):
    r = set()
    for x in a:
        r.add(x)
    for x in b:
        # add ignores the duplicates already in a
        r.add(x)
    return r


def jaccard(a, b):
    common = len(intersection(a, b))
    # |union| = |a| + |b| - |intersection|, no need to build the union
    total = len(a) + len(b) - common
    # both sets are empty, so the union is empty too
    if total == 0:
        return 0
    return common / total


def suggest_friends(friends, u):
    # score[g] = number of friends that u and g have in common
    score = {}
    for f in friends[u]:
        for g in friends[f]:
            # skip u itself and the people u already knows
            if g != u and g not in friends[u]:
                if g in score:
                    score[g] = score[g] + 1
                else:
                    score[g] = 1
    return score


def run_tests():
    # (set A, set B, expected intersection, A - B, B - A, jaccard)
    tests = [
        # example of the lab
        ({101, 102, 103, 104, 105}, {103, 104, 106, 107, 108},
         {103, 104}, {101, 102, 105}, {106, 107, 108}, 0.25),
        # no friend in common: the Roma players and the Juventus players
        ({"Totti", "De Rossi"}, {"Del Piero", "Buffon"},
         set(), {"Totti", "De Rossi"}, {"Del Piero", "Buffon"}, 0),
        # same friends
        ({"Giulia", "Marco", "Sofia"}, {"Giulia", "Marco", "Sofia"},
         {"Giulia", "Marco", "Sofia"}, set(), set(), 1),
        # B inside A, A is the bigger set so intersection swaps them
        ({"Giulia", "Marco", "Sofia", "Luca"}, {"Marco", "Sofia"},
         {"Marco", "Sofia"}, {"Giulia", "Luca"}, set(), 0.5),
        # one user without friends
        (set(), {"Nonna Pina", "Zio Gino"}, set(), set(), {"Nonna Pina", "Zio Gino"}, 0),
        # both without friends, the union is empty
        (set(), set(), set(), set(), set(), 0),
    ]

    print("Set operations")
    for a, b, common, only_a, only_b, coefficient in tests:
        i = intersection(a, b)
        d1 = difference(a, b)
        d2 = difference(b, a)
        u = union(a, b)
        j = jaccard(a, b)
        # the results are also checked against the operators of Python
        good = (i == common and d1 == only_a and d2 == only_b and abs(j - coefficient) < 1e-9
                and i == (a & b) and d1 == (a - b) and d2 == (b - a) and u == (a | b))
        if good:
            print("OK", a, b, "-> mutual:", i, "only A:", d1, "only B:", d2, "union size:", len(u), "jaccard:", j)
        else:
            print("FAIL", a, b, "->", i, d1, d2, u, j)

    # small network: every user has a set of friends, and the friendship goes both ways
    friends = {
        "Marco": {"Giulia", "Luca"},
        "Giulia": {"Marco", "Luca", "Sofia"},
        "Luca": {"Marco", "Giulia", "Sofia", "Chiara"},
        "Sofia": {"Giulia", "Luca"},
        "Chiara": {"Luca"},
        # user without friends
        "Nonno Pino": set(),
        # Totti, De Rossi and Pellegrini all know each other
        "Totti": {"De Rossi", "Pellegrini"},
        "De Rossi": {"Totti", "Pellegrini"},
        "Pellegrini": {"Totti", "De Rossi"},
    }

    # (user, expected suggestions with their score)
    suggestion_tests = [
        # Sofia knows Giulia and Luca, Chiara knows only Luca
        ("Marco", {"Sofia": 2, "Chiara": 1}),
        ("Chiara", {"Marco": 1, "Giulia": 1, "Sofia": 1}),
        # no friends, so no friends of friends
        ("Nonno Pino", {}),
        # everybody is already a friend
        ("Totti", {}),
    ]

    print("\nFriend of friend suggestions")
    for user, expected in suggestion_tests:
        result = suggest_friends(friends, user)
        if result == expected:
            print("OK user", user, "->", result)
        else:
            print("FAIL user", user, "->", result, "but expected", expected)


if __name__ == "__main__":
    run_tests()
