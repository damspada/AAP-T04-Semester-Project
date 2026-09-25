# LAB_01

Team 04: Damiano Spadaccini, Nicolò Romanelli

| Exercise | Assigned to | Solution | Time | Space |
| --- | --- | --- | --- | --- |
| 1 - Integer Mirror | Nicolò Romanelli | take the last digit with n mod 10 and remove it with n div 10 | Θ(log n) | O(1) |
| 2 - Balanced Symbols | Damiano Spadaccini | push the openers on a stack, every closer must match the top | Θ(n) | O(n) |
| 3 - Merge Intervals | Nicolò Romanelli | sort by start, then merge in one pass | O(n log n) | O(n) for the sort |
| 4 - Polynomial Evaluation | Damiano Spadaccini | Horner's method | Θ(n) | O(1) |
| 5 - Array Rotation | Nicolò Romanelli | (1) temporary array, (2) one by one, (3) reverse segments | (1) Θ(n), (2) Θ(n·k), (3) Θ(n) | (1) O(n), (2) O(1), (3) O(1) |
| 6 - First Unique Character | Damiano Spadaccini | (1) two passes with a dictionary, (2) one pass with an ordered dictionary | Θ(n) | O(min(n, Σ)) |

Each file can be run alone and prints OK or FAIL for every test:

```
python3 exercise1_integer_mirror.py
python3 exercise2_balanced_symbols.py
python3 exercise3_merge_intervals.py
python3 exercise4_polynomial_eval.py
python3 exercise5_array_rotation.py
python3 exercise6_first_unique.py
```

The report with pseudo-code, answers, complexity analysis and tests is `T04_LAB1_BFM.pdf`.
