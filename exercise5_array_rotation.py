# Exercise 5 - Array Rotation
# Rotate an array v of size n to the right by k positions.
# Three approaches: temporary array, one by one, reverse segments.


# 1 - TEMPORARY ARRAY: O(n) time, O(n) extra space
def rotate_temp_array(v, n, k):
    if n == 0:
        return
    k = k % n
    temp = [None] * n

    # the element at index i belongs at index (i + k) mod n
    for i in range(n):
        temp[(i + k) % n] = v[i]

    # copy the result back into v
    for i in range(n):
        v[i] = temp[i]


# 2 - ONE BY ONE: O(n * k) time, O(1) extra space
def shift_right_by_one(v, n):
    # the last cell is about to be overwritten, so save it first
    last = v[n - 1]

    # copy each cell from its left neighbour, walking from the end towards the front
    i = n - 1
    while i >= 1:
        v[i] = v[i - 1]
        i = i - 1

    # the saved cell wraps around to the front
    v[0] = last


def rotate_one_by_one(v, n, k):
    if n == 0:
        return
    k = k % n
    for j in range(k):
        shift_right_by_one(v, n)


# 3 - REVERSE SEGMENTS: O(n) time, O(1) extra space
def reverse(v, left, right):
    # walk the two ends towards each other, swapping as they go
    while left < right:
        temp = v[left]
        v[left] = v[right]
        v[right] = temp
        left = left + 1
        right = right - 1


def rotate_reversal(v, n, k):
    if n == 0:
        return
    k = k % n
    if k == 0:
        return
    reverse(v, 0, n - 1)
    reverse(v, 0, k - 1)
    reverse(v, k, n - 1)


def run_tests():
    # (array, k, expected result)
    tests = [
        # k bigger than n
        ([1, 2, 3, 4, 5, 6, 7], 10, [5, 6, 7, 1, 2, 3, 4]),
        ([1], 5, [1]),
        # empty array
        ([], 3, []),
        # k = 0
        ([1, 2, 3], 0, [1, 2, 3]),
        # k = n
        ([1, 2, 3, 4], 4, [1, 2, 3, 4]),
        # negative k, rotation to the left
        ([1, 2, 3, 4, 5], -1, [2, 3, 4, 5, 1]),
    ]

    for v, k, expected in tests:
        # each method works on its own copy of the array
        a = list(v)
        b = list(v)
        c = list(v)
        rotate_temp_array(a, len(a), k)
        rotate_one_by_one(b, len(b), k)
        rotate_reversal(c, len(c), k)
        if a == expected and b == expected and c == expected:
            print("OK", v, "k =", k, "->", a)
        else:
            print("FAIL", v, "k =", k, "->", a, b, c, "but expected", expected)


if __name__ == "__main__":
    run_tests()
