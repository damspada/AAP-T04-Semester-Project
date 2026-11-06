# LAB_04

Team 04: Damiano Spadaccini, Nicolò Romanelli

| Exercise | Assigned to | Solution | Time | Space |
| --- | --- | --- | --- | --- |
| 1 - Recursive Comment Thread Traversal | Damiano Spadaccini | every function calls itself on each reply of the comment | O(n) for n comments | O(d) call stack, d = depth |
| 2 - Recursive Content Aggregation | Nicolò Romanelli | divide and conquer: split posts[left..right] in two halves | O(n) for max, sum, count, O(n log n) for merge sort | O(log n) call stack, O(n) for merge |
| 3 - Recursion to Iteration | Damiano Spadaccini | explicit stack of pairs (comment, state) instead of the call stack | O(n) | O(n) explicit stack in the worst case |

Each file can be run alone and prints OK or FAIL for every test:

```
python3 exercise1_comment_thread.py
python3 exercise2_divide_conquer.py
python3 exercise3_recursion_to_iteration.py
```

The report with pseudo-code, answers, complexity analysis and tests is `T04_LAB4_BFM.pdf`.
