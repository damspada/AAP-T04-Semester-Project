# Exercise 3 - Engagement-Based Priority Queue
# The priority queue is a singly linked list sorted by engagement_score, from the highest to the lowest.
# None is used as the NULL pointer of the pseudo-code.

import random


class Post:
    def __init__(self, post_id, user_id, content, timestamp, likes, comments, shares):
        self.post_id = post_id
        self.user_id = user_id
        self.content = content
        self.timestamp = timestamp
        self.likes = likes
        self.comments = comments
        self.shares = shares
        self.engagement_score = score(self)
        self.next = None


class PriorityQueue:
    def __init__(self):
        self.head = None
        self.count = 0


def score(p):
    return p.likes * 1 + p.comments * 2 + p.shares * 3


def enqueue(Q, p):
    # p goes before the first post with a smaller score
    if Q.head is None or p.engagement_score > Q.head.engagement_score:
        p.next = Q.head
        Q.head = p
    else:
        q = Q.head
        while q.next is not None and q.next.engagement_score >= p.engagement_score:
            q = q.next
        p.next = q.next
        q.next = p
    Q.count = Q.count + 1


def dequeue_max(Q):
    # None if the queue is empty
    p = Q.head
    if p is not None:
        Q.head = p.next
        p.next = None
        Q.count = Q.count - 1
    return p


def peek_max(Q):
    return Q.head


def is_empty(Q):
    return Q.head is None


def size(Q):
    return Q.count


# takes the post out of the queue and returns it (None if it is not in the queue)
def remove_by_id(Q, post_id):
    prev = None
    p = Q.head
    while p is not None and p.post_id != post_id:
        prev = p
        p = p.next
    if p is not None:
        if prev is None:
            Q.head = p.next
        else:
            prev.next = p.next
        p.next = None
        Q.count = Q.count - 1
    return p


# new_likes, new_comments and new_shares are added to the old values
def update_score(Q, post_id, new_likes, new_comments, new_shares):
    updated = False
    p = remove_by_id(Q, post_id)
    if p is not None:
        p.likes = p.likes + new_likes
        p.comments = p.comments + new_comments
        p.shares = p.shares + new_shares
        p.engagement_score = score(p)
        # the post goes back in the right position
        enqueue(Q, p)
        updated = True
    return updated


def refresh_all(Q):
    p = Q.head
    # the queue is emptied and every post is inserted again with its new score
    Q.head = None
    Q.count = 0
    while p is not None:
        next_post = p.next
        p.engagement_score = score(p)
        enqueue(Q, p)
        p = next_post


def get_top_k(Q, k):
    result = []
    p = Q.head
    i = 0
    # there can be fewer than k posts
    while p is not None and i < k:
        result.append(p)
        p = p.next
        i = i + 1
    return result


# factor is between 0 and 1, for example 0.8 to remove 20% of the score
# update_score and refresh_all compute the score again from likes, comments and shares, so after them the decay is lost
def decay_older_than(Q, t, factor):
    p = Q.head
    while p is not None:
        if p.timestamp < t:
            p.engagement_score = p.engagement_score * factor
        p = p.next
    # the order can be wrong now, so every post is inserted again
    p = Q.head
    Q.head = None
    Q.count = 0
    while p is not None:
        next_post = p.next
        enqueue(Q, p)
        p = next_post


# BONUS - DUAL-PRIORITY QUEUE

class DualQueue:
    def __init__(self):
        self.viral_queue = PriorityQueue()
        self.normal_queue = PriorityQueue()


def dual_enqueue(D, p):
    if p.engagement_score > 100:
        enqueue(D.viral_queue, p)
    else:
        enqueue(D.normal_queue, p)


# random.random() gives a real number between 0 and 1
def dual_dequeue(D):
    # if one queue is empty we take from the other one
    if is_empty(D.viral_queue):
        p = dequeue_max(D.normal_queue)
    elif is_empty(D.normal_queue):
        p = dequeue_max(D.viral_queue)
    elif random.random() < 0.7:
        p = dequeue_max(D.viral_queue)
    else:
        p = dequeue_max(D.normal_queue)
    return p


def queue_list(Q):
    out = []
    p = Q.head
    while p is not None:
        out.append((p.post_id, round(p.engagement_score, 2)))
        p = p.next
    return out


def ids(posts):
    out = []
    for p in posts:
        out.append(p.post_id)
    return out


def check(name, result, expected):
    if result == expected:
        print("OK", name, "->", result)
    else:
        print("FAIL", name, "->", result, "but expected", expected)


def lab_queue():
    # the scores of the example: Post1 82, Post2 47, Post3 95, Post4 23
    # Post3 is the only post older than time 50
    Q = PriorityQueue()
    enqueue(Q, Post(1, 11, "Carbonara", 100, 40, 12, 6))
    enqueue(Q, Post(2, 12, "Tiramisu", 100, 20, 6, 5))
    enqueue(Q, Post(3, 13, "Pizza margherita", 0, 50, 15, 5))
    enqueue(Q, Post(4, 14, "Cannoli", 100, 10, 5, 1))
    return Q


def run_tests():
    print("Example of the lab")
    Q = lab_queue()
    check("initial queue", queue_list(Q), [(3, 95), (1, 82), (2, 47), (4, 23)])
    update_score(Q, 2, 10, 0, 0)
    check("Post2 gets 10 new likes", queue_list(Q), [(3, 95), (1, 82), (2, 57), (4, 23)])
    decay_older_than(Q, 50, 0.8)
    check("decay of Post3 by 20%", queue_list(Q), [(1, 82), (3, 76), (2, 57), (4, 23)])

    print("\nCore operations")
    check("peek_max", peek_max(Q).post_id, 1)
    check("dequeue_max", dequeue_max(Q).post_id, 1)
    check("size after dequeue_max", size(Q), 3)
    check("get_top_k(2)", ids(get_top_k(Q, 2)), [3, 2])
    check("get_top_k bigger than the queue", len(get_top_k(Q, 10)), 3)
    check("get_top_k(0)", get_top_k(Q, 0), [])
    E = PriorityQueue()
    check("dequeue_max on an empty queue", dequeue_max(E), None)
    check("peek_max on an empty queue", peek_max(E), None)

    print("\nUpdates")
    Q = lab_queue()
    check("update_score of a post that does not exist", update_score(Q, 9, 5, 0, 0), False)
    # Post4 goes from 23 to 23 + 100 = 123 and becomes the first one
    update_score(Q, 4, 0, 50, 0)
    check("update_score moves a post to the top", queue_list(Q)[0], (4, 123))
    check("size does not change", size(Q), 4)
    decay_older_than(Q, 50, 0.8)
    refresh_all(Q)
    # refresh_all computes the scores again, so the decay of Post3 is lost
    check("refresh_all after the decay", queue_list(Q), [(4, 123), (3, 95), (1, 82), (2, 47)])
    decay_older_than(Q, 0, 0.8)
    check("decay with no old post", queue_list(Q), [(4, 123), (3, 95), (1, 82), (2, 47)])

    print("\nEqual scores")
    Q = PriorityQueue()
    enqueue(Q, Post(1, 11, "Spritz", 1, 10, 0, 0))
    enqueue(Q, Post(2, 12, "Negroni", 2, 10, 0, 0))
    enqueue(Q, Post(3, 13, "Bellini", 3, 4, 3, 0))
    # all have score 10: they keep the arrival order
    check("equal scores", queue_list(Q), [(1, 10), (2, 10), (3, 10)])

    print("\nBonus - dual queue")
    D = DualQueue()
    dual_enqueue(D, Post(1, 11, "Gol di Totti", 1, 101, 0, 0))
    dual_enqueue(D, Post(2, 12, "Lasagna", 1, 100, 0, 0))
    # 101 > 100 goes to viral, 100 stays in normal
    check("score 101 and 100", (size(D.viral_queue), size(D.normal_queue)), (1, 1))
    E = DualQueue()
    dual_enqueue(E, Post(3, 13, "Arancini", 1, 5, 0, 0))
    check("viral queue empty", dual_dequeue(E).post_id, 3)
    check("both queues empty", dual_dequeue(E), None)
    # 1000 dequeues: about 70% must come from the viral queue
    random.seed(4)
    D = DualQueue()
    for i in range(1000):
        dual_enqueue(D, Post(i, 0, "viral", 1, 200, 0, 0))
        dual_enqueue(D, Post(1000 + i, 0, "normal", 1, 50, 0, 0))
    viral = 0
    for i in range(1000):
        if dual_dequeue(D).engagement_score > 100:
            viral = viral + 1
    print("   viral posts out of 1000:", viral)
    check("about 70% viral (between 650 and 750)", 650 <= viral <= 750, True)


if __name__ == "__main__":
    run_tests()
