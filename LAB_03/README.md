# LAB_03

Team 04: Damiano Spadaccini, Nicolò Romanelli

| Exercise | Assigned to | Solution | Time | Space |
| --- | --- | --- | --- | --- |
| 1 - Content Feed Navigation | Nicolò Romanelli | doubly linked list with head, tail and current | O(1) to move, O(n) to find a story | O(n) |
| 2 - Activity Feed Processing | Damiano Spadaccini | stack and queue made of linked nodes, the processor moves notifications from the queue to the stack | O(1) for push, pop, enqueue and dequeue | O(n) |
| 3 - Engagement-Based Priority Queue | Nicolò Romanelli | singly linked list sorted by engagement score | O(n) for enqueue, O(1) for dequeue_max | O(n) |

Each file can be run alone and prints OK or FAIL for every test:

```
python3 exercise1_content_feed.py
python3 exercise2_activity_feed.py
python3 exercise3_priority_queue.py
```

The report with pseudo-code, answers, complexity analysis and tests is `T04_LAB3_BFM.pdf`.
