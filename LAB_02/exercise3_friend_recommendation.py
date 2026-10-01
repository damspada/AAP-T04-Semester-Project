# Exercise 3 - Friend Recommendation by Common Interests
# M is the U x I user-interest matrix (values from 0 to 10), as a list of rows:
# M[v] is the profile of user v, and a 0 means that the interest is not rated.

import math

def cosine_similarity(a, b, n):
    dot = 0
    norm_a = 0
    norm_b = 0
    for j in range(n):
        dot = dot + a[j] * b[j]
        norm_a = norm_a + a[j] * a[j]
        norm_b = norm_b + b[j] * b[j]
    if norm_a == 0 or norm_b == 0:
        # a zero vector is similar to nothing
        return 0
    return dot / (math.sqrt(norm_a) * math.sqrt(norm_b))


def get_score(pair):
    return pair[1]


def top_k_similar_users(M, u, friends, K):
    U = len(M)
    I = len(M[u])
    candidates = []
    for v in range(U):
        # skip u itself and the users already friends of u
        if v != u and v not in friends:
            s = cosine_similarity(M[u], M[v], I)
            candidates.append((v, s))
    candidates.sort(key=get_score, reverse=True)
    # there can be fewer than K candidates
    return candidates[0:min(K, len(candidates))]


def recommend_interests(M, u, neighbors):
    I = len(M[u])
    recommendations = []
    for j in range(I):
        # 0 means "not rated": the matrix has no other value for a missing rating
        if M[u][j] == 0:
            num = 0
            den = 0
            # neighbors holds the pairs (v, s) given by top_k_similar_users
            for v, s in neighbors:
                if M[v][j] > 0:
                    num = num + s * M[v][j]
                    den = den + s
            if den > 0:
                # weighted average of the values of the neighbors
                predicted = num / den
                recommendations.append((j, predicted))
    recommendations.sort(key=get_score, reverse=True)
    return recommendations


def column(M, j):
    # a column has U values, one for each user
    col = []
    for v in range(len(M)):
        col.append(M[v][j])
    return col


def group_interests(M, threshold):
    U = len(M)
    I = len(M[0])
    groups = []
    assigned = [False] * I
    for j in range(I):
        if not assigned[j]:
            group = {j}
            assigned[j] = True
            for k in range(j + 1, I):
                if not assigned[k]:
                    if cosine_similarity(column(M, j), column(M, k), U) >= threshold:
                        group.add(k)
                        assigned[k] = True
            groups.append(group)
    return groups


def reduce_matrix(M, groups):
    # each group becomes one column of the new matrix, the average of its interests
    R = []
    for v in range(len(M)):
        row = []
        for group in groups:
            total = 0
            for j in group:
                total = total + M[v][j]
            row.append(total / len(group))
        R.append(row)
    return R


def close(a, b):
    # floats are not always exact, so we accept a small difference
    return abs(a - b) < 1e-2


def close_pairs(result, expected):
    if len(result) != len(expected):
        return False
    for k in range(len(result)):
        if result[k][0] != expected[k][0] or not close(result[k][1], expected[k][1]):
            return False
    return True


def rounded(pairs):
    out = []
    for v, s in pairs:
        out.append((v, round(s, 2)))
    return out


def run_tests():
    # interests: Music, Sports, Tech, Fashion, Travel, Food
    M = [
        [10, 0, 8, 2, 5, 7],   # user 0, example of the lab
        [9, 1, 7, 3, 6, 8],    # user 1, example of the lab
        [2, 9, 1, 8, 3, 0],    # user 2, example of the lab
        [8, 0, 9, 0, 4, 6],    # user 3, Leonardo da Vinci: music, tech and food, no Sports and no Fashion
        [0, 0, 0, 0, 0, 0],    # user 4, Nonno Pino: no interest at all
        [0, 10, 0, 9, 0, 0],   # user 5, Totti: only Sports and Fashion
    ]

    # (a, b, expected similarity)
    similarity_tests = [
        # examples of the lab
        (M[0], M[1], 0.99),
        (M[0], M[2], 0.30),
        # the same profile
        (M[0], M[0], 1.0),
        # zero vector
        (M[0], M[4], 0),
        # no interest in common
        (M[3], M[5], 0),
        # Mario and Luigi have the same tastes, Luigi just gives double values
        ([1, 2, 3], [2, 4, 6], 1.0),
    ]

    print("Cosine similarity")
    for a, b, expected in similarity_tests:
        result = cosine_similarity(a, b, len(a))
        if close(result, expected):
            print("OK", a, b, "->", round(result, 2))
        else:
            print("FAIL", a, b, "->", result, "but expected", expected)

    # (user, friends, K, expected list of (user, similarity))
    top_k_tests = [
        # user 1 is already a friend of user 0
        (0, {1}, 2, [(3, 0.98), (2, 0.30)]),
        # K bigger than the number of candidates
        (0, {1, 2}, 10, [(3, 0.98), (5, 0.09), (4, 0)]),
        # K = 0
        (0, set(), 0, []),
        # every other user is already a friend
        (0, {1, 2, 3, 4, 5}, 3, []),
        # Nonno Pino is similar to nobody
        (4, set(), 2, [(0, 0), (1, 0)]),
    ]

    print("\nTop K similar users")
    for u, friends, K, expected in top_k_tests:
        result = top_k_similar_users(M, u, friends, K)
        if close_pairs(result, expected):
            print("OK user", u, "friends", friends, "K =", K, "->", rounded(result))
        else:
            print("FAIL user", u, "->", rounded(result), "but expected", expected)

    # (user, neighbors, expected list of (interest, predicted value))
    recommend_tests = [
        # Leonardo (user 3) has not rated Sports (1) and Fashion (3)
        (3, top_k_similar_users(M, 3, set(), 2), [(3, 2.49), (1, 1.0)]),
        # with user 2 among the neighbors Leonardo gets higher values for Sports and Fashion
        (3, top_k_similar_users(M, 3, set(), 3), [(3, 3.03), (1, 2.44)]),
        # user 1 has rated every interest, nothing to recommend
        (1, top_k_similar_users(M, 1, set(), 2), []),
        # no neighbor
        (3, [], []),
        # the only neighbor has similarity 0, so it gives no information
        (4, [(0, 0)], []),
    ]

    print("\nRecommended interests")
    for u, neighbors, expected in recommend_tests:
        result = recommend_interests(M, u, neighbors)
        if close_pairs(result, expected):
            print("OK user", u, "neighbors", rounded(neighbors), "->", rounded(result))
        else:
            print("FAIL user", u, "->", rounded(result), "but expected", expected)

    # (threshold, expected groups of interests)
    group_tests = [
        (0.8, [{0, 2, 4, 5}, {1, 3}]),
        # every similarity is >= 0, so everything is in one group
        (0.0, [{0, 1, 2, 3, 4, 5}]),
        # a similarity is never bigger than 1, so every interest is alone
        (1.1, [{0}, {1}, {2}, {3}, {4}, {5}]),
    ]

    print("\nGroups of interests")
    for threshold, expected in group_tests:
        result = group_interests(M, threshold)
        if result == expected:
            print("OK threshold", threshold, "->", result)
        else:
            print("FAIL threshold", threshold, "->", result, "but expected", expected)

    # the 6 interests become 2: (Music, Tech, Travel, Food) and (Sports, Fashion)
    groups = group_interests(M, 0.8)
    R = reduce_matrix(M, groups)
    expected = [[7.5, 1.0], [7.5, 2.0], [1.5, 8.5], [6.75, 0.0], [0.0, 0.0], [0.0, 9.5]]
    if R == expected:
        print("OK reduced matrix", R)
    else:
        print("FAIL reduced matrix", R, "but expected", expected)
    # the similarity between user 0 and user 1 stays almost the same with 2 columns instead of 6
    print("similarity user 0 - user 1 with 6 interests:", round(cosine_similarity(M[0], M[1], 6), 3),
          "with 2 groups:", round(cosine_similarity(R[0], R[1], 2), 3))


if __name__ == "__main__":
    run_tests()
