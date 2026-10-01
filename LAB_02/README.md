# LAB_02

Team 04: Damiano Spadaccini, Nicolò Romanelli

| Exercise | Assigned to | Solution | Time | Space |
| --- | --- | --- | --- | --- |
| 1 - Friend Request Timeline | Nicolò Romanelli | read the message once and update all the counters | Θ(n) | O(1) |
| 2 - Mutual Friends Detection | Damiano Spadaccini | hash sets, the intersection walks the smaller set | Θ(min(m, n)) for the intersection | O(m + n) |
| 3 - Friend Recommendation | Nicolò Romanelli | cosine similarity between the rows of the matrix, then sort for the top K | O(U·I + U log U) for the top K | O(U·I) |
| 4 - Mutual Followers Matrix | Damiano Spadaccini | boolean matrix, row u = following, column u = followers | Θ(n) for followers and following | Θ(N²) |

Each file can be run alone and prints OK or FAIL for every test:

```
python3 exercise1_friend_request_timeline.py
python3 exercise2_mutual_friends.py
python3 exercise3_friend_recommendation.py
python3 exercise4_follower_matrix.py
```

The report with pseudo-code, answers, complexity analysis and tests is `T04_LAB2_BFM.pdf`.
