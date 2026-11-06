# Exercise 2 - Recursive Content Aggregation with Divide & Conquer
# Every function works on the part posts[left .. right] and splits it in two halves.

import random


class Post:
    def __init__(self, post_id, user_id, content_preview, timestamp, likes, comments, shares):
        self.post_id = post_id
        self.user_id = user_id
        self.content_preview = content_preview
        self.timestamp = timestamp
        self.likes = likes
        self.comments = comments
        self.shares = shares
        self.engagement_score = score(self)


def score(p):
    return p.likes * 1 + p.comments * 2 + p.shares * 3


# PART A - MAXIMUM ENGAGEMENT

# returns the position of the post with the highest score, so we know the post and its score
def max_engagement(posts, left, right):
    if left == right:
        return left
    mid = (left + right) // 2
    a = max_engagement(posts, left, mid)
    b = max_engagement(posts, mid + 1, right)
    if posts[a].engagement_score >= posts[b].engagement_score:
        best = a
    else:
        best = b
    return best


# PART B - TOTAL AND AVERAGE

def sum_engagement(posts, left, right):
    if left > right:
        # empty part
        return 0
    if left == right:
        return posts[left].engagement_score
    mid = (left + right) // 2
    return sum_engagement(posts, left, mid) + sum_engagement(posts, mid + 1, right)


def average_engagement(posts, left, right):
    n = right - left + 1
    average = 0
    if n > 0:
        average = sum_engagement(posts, left, right) / n
    return average


# PART C - COUNT BY THRESHOLD

def count_above_threshold(posts, left, right, threshold):
    if left > right:
        return 0
    if left == right:
        count = 0
        if posts[left].engagement_score > threshold:
            count = 1
        return count
    mid = (left + right) // 2
    return (count_above_threshold(posts, left, mid, threshold)
            + count_above_threshold(posts, mid + 1, right, threshold))


# PART D - MERGE SORT BY ENGAGEMENT (from the highest to the lowest score)

# number of comparisons of scores, used to compare merge sort and insertion sort
comparisons = 0


def merge_sort_by_engagement(posts, left, right):
    if left < right:
        mid = (left + right) // 2
        merge_sort_by_engagement(posts, left, mid)
        merge_sort_by_engagement(posts, mid + 1, right)
        merge(posts, left, mid, right)


def merge(posts, left, mid, right):
    global comparisons
    temp = []
    i = left
    j = mid + 1
    while i <= mid and j <= right:
        comparisons = comparisons + 1
        # with ">=" two posts with the same score keep their order
        if posts[i].engagement_score >= posts[j].engagement_score:
            temp.append(posts[i])
            i = i + 1
        else:
            temp.append(posts[j])
            j = j + 1
    # copy the rest of the half that is not finished
    while i <= mid:
        temp.append(posts[i])
        i = i + 1
    while j <= right:
        temp.append(posts[j])
        j = j + 1
    for k in range(left, right + 1):
        posts[k] = temp[k - left]


def lower_score(a, b):
    global comparisons
    comparisons = comparisons + 1
    return a.engagement_score < b.engagement_score


def insertion_sort_by_engagement(posts):
    # iterative version, only to compare the number of comparisons with merge sort
    for i in range(1, len(posts)):
        p = posts[i]
        j = i - 1
        # move to the right the posts with a lower score than p
        while j >= 0 and lower_score(posts[j], p):
            posts[j + 1] = posts[j]
            j = j - 1
        posts[j + 1] = p


# PEAK HOUR

# the likes must increase until the peak and then decrease
def find_peak_hour(likes, left, right):
    if left == right:
        return left
    mid = (left + right) // 2
    if likes[mid] < likes[mid + 1]:
        # likes[mid + 1] is bigger, so the peak is on the right
        peak = find_peak_hour(likes, mid + 1, right)
    else:
        # otherwise the peak is mid or on the left
        peak = find_peak_hour(likes, left, mid)
    return peak


def ids(posts):
    out = []
    for p in posts:
        out.append(p.post_id)
    return out


def lab_posts():
    # scores of the example: 150, 320, 95, 280
    return [Post(1, 11, "Carbonara", 1, 100, 16, 6),
            Post(2, 12, "Tiramisu", 2, 200, 30, 20),
            Post(3, 13, "Pizza", 3, 50, 15, 5),
            Post(4, 14, "Lasagna", 4, 160, 30, 20)]


def random_posts(n):
    posts = []
    for i in range(n):
        posts.append(Post(i, 0, "post", i, random.randint(0, 500), random.randint(0, 100), random.randint(0, 50)))
    return posts


def check(name, result, expected):
    if result == expected:
        print("OK", name, "->", result)
    else:
        print("FAIL", name, "->", result, "but expected", expected)


def run_tests():
    global comparisons
    print("Example of the lab")
    posts = lab_posts()
    best = max_engagement(posts, 0, 3)
    check("max_engagement", (posts[best].post_id, posts[best].engagement_score), (2, 320))
    check("sum_engagement", sum_engagement(posts, 0, 3), 845)
    check("average_engagement", average_engagement(posts, 0, 3), 211.25)
    check("count_above_threshold 200", count_above_threshold(posts, 0, 3, 200), 2)
    merge_sort_by_engagement(posts, 0, 3)
    check("merge_sort_by_engagement", ids(posts), [2, 4, 1, 3])

    print("\nEdge cases")
    posts = lab_posts()
    check("max of a single post", max_engagement(posts, 2, 2), 2)
    check("sum of an empty part", sum_engagement(posts, 3, 2), 0)
    check("average of an empty part", average_engagement(posts, 3, 2), 0)
    check("count with threshold equal to a score (strictly greater)", count_above_threshold(posts, 0, 3, 320), 0)
    check("count with a negative threshold", count_above_threshold(posts, 0, 3, -1), 4)
    same = [Post(1, 0, "a", 1, 10, 0, 0), Post(2, 0, "b", 2, 10, 0, 0), Post(3, 0, "c", 3, 10, 0, 0)]
    check("max with equal scores (the first one)", same[max_engagement(same, 0, 2)].post_id, 1)
    merge_sort_by_engagement(same, 0, 2)
    check("merge sort with equal scores keeps the order", ids(same), [1, 2, 3])
    one = [Post(7, 0, "x", 1, 1, 1, 1)]
    merge_sort_by_engagement(one, 0, 0)
    check("merge sort of one post", ids(one), [7])
    sorted_posts = random_posts(200)
    merge_sort_by_engagement(sorted_posts, 0, 199)
    ok = True
    for i in range(199):
        if sorted_posts[i].engagement_score < sorted_posts[i + 1].engagement_score:
            ok = False
    check("merge sort of 200 random posts is sorted", ok, True)

    print("\nPeak hour")
    likes = [5, 8, 12, 25, 30, 28, 15, 10, 9, 8, 7, 6, 6, 5, 5, 4, 4, 3, 3, 2, 2, 1, 1, 0]
    check("peak of the lab example", find_peak_hour(likes, 0, 23), 4)
    up = []
    for h in range(24):
        up.append(h)
    check("likes only increase: last hour", find_peak_hour(up, 0, 23), 23)
    down = []
    for h in range(24):
        down.append(24 - h)
    check("likes only decrease: first hour", find_peak_hour(down, 0, 23), 0)
    check("only one hour", find_peak_hour([42], 0, 0), 0)
    # two peaks: the function finds a peak, not always the biggest one
    two = [1, 9, 2, 3, 4, 5, 6, 7]
    check("two peaks: it finds the local peak at the end", find_peak_hour(two, 0, 7), 7)

    print("\nMerge sort vs insertion sort (comparisons of scores)")
    random.seed(1)
    for n in [100, 1000, 3000, 10000]:
        posts = random_posts(n)
        comparisons = 0
        merge_sort_by_engagement(posts, 0, n - 1)
        merge_count = comparisons
        if n <= 3000:
            posts = random_posts(n)
            comparisons = 0
            insertion_sort_by_engagement(posts)
            insertion_count = comparisons
        else:
            # 10 000 posts with insertion sort are slow in Python: about n^2 / 4 comparisons
            insertion_count = n * n // 4
        print("  n =", n, " merge sort:", merge_count, " insertion sort:", insertion_count)


if __name__ == "__main__":
    run_tests()
