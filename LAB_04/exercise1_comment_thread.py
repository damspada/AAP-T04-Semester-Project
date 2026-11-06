# Exercise 1 - Recursive Comment Thread Traversal
# A thread is a tree: every comment has a list of replies, and every reply is a comment too.
# None is used as the NULL pointer of the pseudo-code.


class CommentNode:
    def __init__(self, comment_id, user_id, content, timestamp, likes):
        self.comment_id = comment_id
        self.user_id = user_id
        self.content = content[:100]      # content is limited to 100 characters
        self.timestamp = timestamp
        self.likes = likes
        self.replies = []


def display_thread(c, level):
    # the shown lines are also returned, so the tests can check them
    lines = []
    if c is not None:
        # 2 spaces for each level
        line = "  " * level + c.user_id + ": " + c.content
        print(line)
        lines.append(line)
        for r in c.replies:
            for x in display_thread(r, level + 1):
                lines.append(x)
    return lines


def count_total_comments(c):
    total = 0
    if c is not None:
        # the comment itself and all the comments in its replies
        total = 1
        for r in c.replies:
            total = total + count_total_comments(r)
    return total


def total_likes(c):
    likes = 0
    if c is not None:
        likes = c.likes
        for r in c.replies:
            likes = likes + total_likes(r)
    return likes


# c must not be None, a comment without replies has depth 0
def find_deepest_reply(c):
    deepest = 0
    for r in c.replies:
        d = 1 + find_deepest_reply(r)
        if d > deepest:
            deepest = d
    return deepest


def search_by_user(user_id, c):
    result = []
    collect_by_user(user_id, c, result)
    return result


def collect_by_user(user_id, c, result):
    # all the comments go in the same list, so no list is copied
    if c is not None:
        if c.user_id == user_id:
            result.append(c)
        for r in c.replies:
            collect_by_user(user_id, r, result)


def contains_keyword(keyword, c):
    found = False
    if c is not None:
        if keyword in c.content:
            found = True
        i = 0
        # stop as soon as the keyword is found
        while not found and i < len(c.replies):
            found = contains_keyword(keyword, c.replies[i])
            i = i + 1
    return found


def delete_comment(comment_id, thread):
    if thread is None:
        return None
    if thread.comment_id == comment_id:
        # the comment and all its replies go away
        return None
    new_replies = []
    for r in thread.replies:
        kept = delete_comment(comment_id, r)
        if kept is not None:
            new_replies.append(kept)
    thread.replies = new_replies
    return thread


def ids(comments):
    out = []
    for c in comments:
        out.append(c.comment_id)
    return out


def lab_thread():
    # the example of the lab
    c101 = CommentNode(101, "Alice", "This recipe looks amazing!", 1, 10)
    c201 = CommentNode(201, "Bob", "I tried it last night!", 2, 5)
    c301 = CommentNode(301, "Alice", "What did you think?", 3, 2)
    c401 = CommentNode(401, "Bob", "It was delicious!", 4, 7)
    c202 = CommentNode(202, "Charlie", "Can I use olive oil instead?", 5, 3)
    c302 = CommentNode(302, "Alice", "Yes, that works too!", 6, 1)
    c101.replies = [c201, c202]
    c201.replies = [c301]
    c301.replies = [c401]
    c202.replies = [c302]
    return c101


def check(name, result, expected):
    if result == expected:
        print("OK", name, "->", result)
    else:
        print("FAIL", name, "->", result, "but expected", expected)


def run_tests():
    print("Example of the lab")
    t = lab_thread()
    lines = display_thread(t, 0)
    check("display: first line", lines[0], "Alice: This recipe looks amazing!")
    check("display: reply at level 3 has 6 spaces", lines[3], "      Bob: It was delicious!")
    check("count_total_comments", count_total_comments(t), 6)
    check("total_likes", total_likes(t), 28)
    check("find_deepest_reply", find_deepest_reply(t), 3)
    check("search_by_user Alice", ids(search_by_user("Alice", t)), [101, 301, 302])
    check("search_by_user Charlie", ids(search_by_user("Charlie", t)), [202])
    check("contains_keyword olive", contains_keyword("olive", t), True)
    check("contains_keyword in the deepest reply", contains_keyword("delicious", t), True)

    print("\nEdge cases")
    check("search_by_user that never commented", search_by_user("Dave", t), [])
    check("contains_keyword not in the thread", contains_keyword("pizza", t), False)
    check("contains_keyword is case sensitive", contains_keyword("Olive", t), False)
    check("count of an empty thread", count_total_comments(None), 0)
    check("likes of an empty thread", total_likes(None), 0)
    single = CommentNode(1, "Marco", "Ciao a tutti", 1, 4)
    check("single comment: count", count_total_comments(single), 1)
    check("single comment: deepest", find_deepest_reply(single), 0)
    long_text = CommentNode(2, "Giulia", "a" * 150, 1, 0)
    check("content limited to 100 characters", len(long_text.content), 100)

    print("\nDelete with cascade")
    t = lab_thread()
    t = delete_comment(201, t)
    # 201, 301 and 401 are removed
    check("delete 201: comments left", ids(search_by_user("Alice", t)) + ids(search_by_user("Charlie", t)), [101, 302, 202])
    check("delete 201: count", count_total_comments(t), 3)
    check("delete 201: deepest", find_deepest_reply(t), 2)
    t = delete_comment(999, t)
    check("delete a comment that does not exist", count_total_comments(t), 3)
    t = delete_comment(302, t)
    check("delete a leaf", count_total_comments(t), 2)
    check("delete the first comment", delete_comment(101, t), None)
    check("delete in an empty thread", delete_comment(1, None), None)


if __name__ == "__main__":
    run_tests()
