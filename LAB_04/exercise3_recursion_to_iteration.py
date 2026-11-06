# Exercise 3 - Converting Recursion to Iteration with Explicit Stack
# The same comment threads of exercise 1; the stack is a Python list used only with append and pop.
# None is used as the NULL pointer of the pseudo-code.

import sys

STATE_START = 0           # just pushed, the replies are not processed yet
STATE_REPLIES_DONE = 1    # all the replies are processed


class CommentNode:
    def __init__(self, comment_id, user_id, content, timestamp, likes):
        self.comment_id = comment_id
        self.user_id = user_id
        self.content = content[:100]      # content is limited to 100 characters
        self.timestamp = timestamp
        self.likes = likes
        self.replies = []


# 1 - RECURSIVE FLATTENER

# number of calls open at the same time, to measure the recursion depth
open_calls = 0
max_open_calls = 0


def flatten_recursive(c):
    result = []
    add_to_list(c, result)
    return result


def add_to_list(c, result):
    global open_calls, max_open_calls
    open_calls = open_calls + 1
    if open_calls > max_open_calls:
        max_open_calls = open_calls
    if c is not None:
        result.append(c)
        for r in c.replies:
            add_to_list(r, result)
    open_calls = open_calls - 1


# 2 - ITERATIVE FLATTENER WITH EXPLICIT STACK

# biggest size reached by the explicit stack
max_stack_size = 0


def flatten_iterative(c):
    global max_stack_size
    result = []
    if c is not None:
        stack = []
        stack.append((c, STATE_START))
        max_stack_size = 1
        while len(stack) > 0:
            x, state = stack.pop()
            if state == STATE_START:
                result.append(x)
                stack.append((x, STATE_REPLIES_DONE))
                # replies in reverse order, so the first reply is popped first
                for i in range(len(x.replies) - 1, -1, -1):
                    stack.append((x.replies[i], STATE_START))
                if len(stack) > max_stack_size:
                    max_stack_size = len(stack)
            # with STATE_REPLIES_DONE there is nothing more to do for x
    return result


# 3 - TAIL RECURSION AND LOOP

# pending = comments still to count; the recursive call is the last thing the function does
def count_comments_tail(pending, accumulator):
    if len(pending) == 0:
        return accumulator
    c = pending.pop()
    for r in c.replies:
        pending.append(r)
    return count_comments_tail(pending, accumulator + 1)


# the same function, where the tail call becomes a new turn of the loop
def count_comments_loop(comment):
    pending = [comment]
    accumulator = 0
    while len(pending) > 0:
        c = pending.pop()
        for r in c.replies:
            pending.append(r)
        accumulator = accumulator + 1
    return accumulator


def count_comments_recursive(c):
    # normal recursion, used to see when the call stack is too small
    total = 1
    for r in c.replies:
        total = total + count_comments_recursive(r)
    return total


def ids(comments):
    out = []
    for c in comments:
        out.append(c.comment_id)
    return out


def lab_thread():
    # the example of the lab: Comment1 -> Reply1 -> SubReply1, and Comment1 -> Reply2
    comment1 = CommentNode(1, "Alice", "Comment1", 1, 0)
    reply1 = CommentNode(2, "Bob", "Reply1", 2, 0)
    sub_reply1 = CommentNode(3, "Alice", "SubReply1", 3, 0)
    reply2 = CommentNode(4, "Charlie", "Reply2", 4, 0)
    comment1.replies = [reply1, reply2]
    reply1.replies = [sub_reply1]
    return comment1


def chain(depth):
    # a thread where every comment has only one reply: depth + 1 comments
    first = CommentNode(0, "Marco", "level 0", 0, 0)
    c = first
    for d in range(1, depth + 1):
        r = CommentNode(d, "Giulia", "level " + str(d), d, 0)
        c.replies = [r]
        c = r
    return first


def star(n):
    # one comment with n - 1 replies and no deeper level
    first = CommentNode(0, "Luca", "post", 0, 0)
    for i in range(1, n):
        first.replies.append(CommentNode(i, "Sofia", "reply", i, 0))
    return first


def check(name, result, expected):
    if result == expected:
        print("OK", name, "->", result)
    else:
        print("FAIL", name, "->", result, "but expected", expected)


def run_tests():
    global max_open_calls
    print("Example of the lab")
    t = lab_thread()
    check("flatten_recursive", ids(flatten_recursive(t)), [1, 2, 3, 4])
    check("flatten_iterative", ids(flatten_iterative(t)), [1, 2, 3, 4])
    check("count_comments_tail", count_comments_tail([t], 0), 4)
    check("count_comments_loop", count_comments_loop(t), 4)

    print("\nEdge cases")
    check("flatten of an empty thread (recursive)", flatten_recursive(None), [])
    check("flatten of an empty thread (iterative)", flatten_iterative(None), [])
    single = CommentNode(9, "Nonno Pino", "ciao", 1, 0)
    check("single comment", ids(flatten_iterative(single)), [9])
    s = star(6)
    check("one comment with 5 replies: same order", ids(flatten_iterative(s)), ids(flatten_recursive(s)))
    check("one comment with 5 replies: stack size", max_stack_size, 6)

    print("\nDepth of the recursion vs size of the explicit stack")
    for depth in [5, 10, 50, 100, 500]:
        t = chain(depth)
        max_open_calls = 0
        a = flatten_recursive(t)
        b = flatten_iterative(t)
        same = ids(a) == ids(b)
        print("  depth", depth, ": recursive calls open at the same time =", max_open_calls,
              " explicit stack max =", max_stack_size, " same result:", same)
        check("depth " + str(depth) + ": same count with the loop", count_comments_loop(t), depth + 1)

    print("\nVery deep thread (2000 levels)")
    print("  Python recursion limit:", sys.getrecursionlimit())
    t = chain(2000)
    crashed = False
    try:
        count_comments_recursive(t)
    except RecursionError:
        crashed = True
    check("recursive count crashes with RecursionError", crashed, True)
    check("iterative flatten still works", len(flatten_iterative(t)), 2001)
    check("loop count still works", count_comments_loop(t), 2001)
    # Python does not remove the tail calls, so also the tail recursive version crashes
    crashed = False
    try:
        count_comments_tail([t], 0)
    except RecursionError:
        crashed = True
    check("tail recursion is not optimized in Python", crashed, True)


if __name__ == "__main__":
    run_tests()
