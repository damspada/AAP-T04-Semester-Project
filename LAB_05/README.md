# LAB_05

Team 04: Damiano Spadaccini, Nicolò Romanelli

| Exercise | Assigned to | Solution | Time | Space |
| --- | --- | --- | --- | --- |
| 1 - Binary Tree Representation of Content Categories | Nicolò Romanelli | recursive metrics, properties with the definitions of the lecture, search with parent pointers | O(n), IsBalanced O(n log n) to O(n^2) | O(H) call stack, O(width) queue for IsPerfect |
| 2 - Tree Traversals for Content Processing | Damiano Spadaccini | in-order, pre-order and post-order, plus iterative pre-order and in-order with an explicit stack | O(n), InOrderFindKth O(H + k) | O(H) call stack, O(n) for the lists |
| 3 - Generalized Trees (N-ary Trees) | Nicolò Romanelli | list of children; first child, next sibling for the binary version; level-order with a queue | O(n) | O(H) call stack, O(width) queue |

Each file can be run alone and prints OK or FAIL for every test:

```
python3 exercise1_binary_tree.py
python3 exercise2_traversals.py
python3 exercise3_generalized_trees.py
```

The report with pseudo-code, answers, complexity analysis and tests is `T04_LAB5_BFM.pdf`.
