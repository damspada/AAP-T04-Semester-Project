# Exercise 4 - Mutual Followers Matrix
# Directed social graph as an adjacency matrix of booleans:
# matrix[i][j] = True means that user i follows user j.
# The users go from 1 to N, as in the pseudo-code, so row 0 and column 0 are not used.


class FollowerMatrix:
    def __init__(self):
        self.matrix = []
        self.size = 0
        self.user_count = 0


def create(N):
    G = FollowerMatrix()
    G.size = N
    G.user_count = 0
    for i in range(N + 1):
        G.matrix.append([False] * (N + 1))
    return G


def add_user(G):
    # -1 means that the matrix is full
    user_id = -1
    if G.user_count < G.size:
        G.user_count = G.user_count + 1
        user_id = G.user_count
    return user_id


def is_user(G, u):
    return u >= 1 and u <= G.user_count


def follow(G, follower, followee):
    # both users must exist, and nobody can follow themselves
    if is_user(G, follower) and is_user(G, followee) and follower != followee:
        G.matrix[follower][followee] = True


def unfollow(G, follower, followee):
    if is_user(G, follower) and is_user(G, followee):
        G.matrix[follower][followee] = False


def is_following(G, follower, followee):
    result = False
    # check the users first, so the matrix is never read outside its bounds
    if is_user(G, follower) and is_user(G, followee):
        result = G.matrix[follower][followee]
    return result


def get_followers(G, u):
    # u must be a user (is_user(G, u) = True)
    # the followers of u are the True cells of column u
    result = []
    for i in range(1, G.user_count + 1):
        if G.matrix[i][u]:
            result.append(i)
    return result


def get_following(G, u):
    # the users that u follows are the True cells of row u
    result = []
    for j in range(1, G.user_count + 1):
        if G.matrix[u][j]:
            result.append(j)
    return result


def mutual_follows(G):
    # every mutual pair only once, with i < j: (1, 2) and (2, 1) are the same pair
    pairs = []
    for i in range(1, G.user_count + 1):
        for j in range(i + 1, G.user_count + 1):
            if G.matrix[i][j] and G.matrix[j][i]:
                pairs.append((i, j))
    return pairs


def influence_score(G, u):
    # u must be a user, so user_count >= 1 and there is no division by zero
    return (len(get_followers(G, u)) + len(get_following(G, u))) / G.user_count


def check(name, result, expected):
    if result == expected:
        print("OK", name, "->", result)
    else:
        print("FAIL", name, "->", result, "but expected", expected)


def run_tests():
    # example of the lab: 1 Romeo follows 2 Giulietta, Giulietta follows Romeo and 3 Paride
    G = create(3)
    for k in range(3):
        add_user(G)
    follow(G, 1, 2)
    follow(G, 2, 1)
    follow(G, 2, 3)

    print("Example of the lab")
    check("followers of Paride", get_followers(G, 3), [2])
    check("following of Giulietta", get_following(G, 2), [1, 3])
    check("following of Paride", get_following(G, 3), [])
    check("mutual follows (Romeo and Giulietta)", mutual_follows(G), [(1, 2)])
    check("influence of Romeo", influence_score(G, 1), 2 / 3)
    check("influence of Giulietta", influence_score(G, 2), 3 / 3)
    # Paride follows nobody but is followed by Giulietta
    check("influence of Paride", influence_score(G, 3), 1 / 3)

    print("\nEdge cases")
    # the matrix is full
    check("add user to a full matrix", add_user(G), -1)
    # nobody can follow themselves
    follow(G, 1, 1)
    check("self follow", is_following(G, 1, 1), False)
    # users that do not exist are ignored, and the matrix is not read outside its bounds
    follow(G, 1, 4)
    check("follow a user that does not exist", is_following(G, 1, 4), False)
    check("is_following with user 0", is_following(G, 0, 1), False)
    # Romeo follows Giulietta two times: nothing changes
    follow(G, 1, 2)
    check("follow two times", get_followers(G, 2), [1])
    # Giulietta unfollows Romeo: the mutual pair is broken
    unfollow(G, 2, 1)
    check("after Giulietta unfollows Romeo", mutual_follows(G), [])
    # Romeo unfollows Paride, but he does not follow him: nothing changes
    unfollow(G, 1, 3)
    check("unfollow when not following", get_following(G, 1), [2])

    # matrix of size 5 with only Mario and Luigi: the loops stop at user_count
    H = create(5)
    add_user(H)
    add_user(H)
    # Peach is the third user
    check("new user id", add_user(H), 3)
    follow(H, 1, 2)
    follow(H, 2, 1)
    check("mutual follows with size > user_count", mutual_follows(H), [(1, 2)])
    check("Peach, user without relations", influence_score(H, 3), 0)

    # the 4 Ninja Turtles (Leonardo, Michelangelo, Donatello, Raffaello) all follow each other:
    # n (n - 1) / 2 mutual pairs and influence 2 (n - 1) / n
    n = 4
    F = create(n)
    for k in range(n):
        add_user(F)
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            follow(F, i, j)
    check("complete network, mutual pairs", len(mutual_follows(F)), 6)
    check("complete network, influence of 1", influence_score(F, 1), 1.5)


if __name__ == "__main__":
    run_tests()
