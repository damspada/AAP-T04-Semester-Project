# Exercise 3 - Merge Overlapping Intervals
# Each interval is a list [start, end] with start <= end.
# The list is sorted by start and then merged in place, in one pass.


def get_start(interval):
    return interval[0]


def merge_overlapping_intervals(intervals):
    n = len(intervals)

    # empty case
    if n == 0:
        return intervals

    # after sorting, overlapping intervals are next to each other
    intervals.sort(key=get_start)

    # position of the current merged block
    last = 0
    for i in range(1, n):
        # ask if the intervals overlap
        if intervals[i][0] <= intervals[last][1]:
            # stretch the block
            intervals[last][1] = max(intervals[last][1], intervals[i][1])
        else:
            last = last + 1
            intervals[last] = intervals[i]

    # the cells after "last" are old intervals already merged, so they are removed
    del intervals[last + 1:]
    return intervals


def run_tests():
    # (input, expected result)
    tests = [
        ([[1, 3], [2, 6], [15, 18], [8, 10]], [[1, 6], [8, 10], [15, 18]]),
        # touching intervals
        ([[1, 4], [4, 5]], [[1, 5]]),
        # not sorted
        ([[1, 4], [0, 4]], [[0, 4]]),
        # empty input
        ([], []),
        # single interval
        ([[3, 7]], [[3, 7]]),
        # no overlaps
        ([[1, 2], [4, 5], [7, 8]], [[1, 2], [4, 5], [7, 8]]),
        # intervals inside another
        ([[1, 10], [2, 3], [4, 5]], [[1, 10]]),
    ]

    for intervals, expected in tests:
        result = merge_overlapping_intervals(intervals)
        if result == expected:
            print("OK", result)
        else:
            print("FAIL", result, "but expected", expected)


if __name__ == "__main__":
    run_tests()
