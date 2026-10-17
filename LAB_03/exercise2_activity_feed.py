# Exercise 2 - Activity Feed Processing with Stacks and Queues
# The stack and the queue are made of linked nodes (value + pointer next), not of Python lists.
# None is used as the NULL pointer of the pseudo-code.


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


# PART A - RECENT ACTIVITY STACK

class ActivityStack:
    def __init__(self):
        self.top = None
        self.count = 0


def push(S, activity):
    node = Node(activity)
    # the new node goes on top of the old top
    node.next = S.top
    S.top = node
    S.count = S.count + 1


def pop(S):
    if S.top is None:
        return None
    activity = S.top.value
    S.top = S.top.next
    S.count = S.count - 1
    return activity


def peek(S):
    if S.top is None:
        return None
    return S.top.value


def is_empty(S):
    return S.top is None


def size(S):
    return S.count


def display_recent(S, n):
    # the shown activities are also returned, so the tests can check them
    shown = []
    p = S.top
    i = 0
    # from the most recent, stop after n activities or at the bottom of the stack
    while p is not None and i < n:
        print("  ", p.value)
        shown.append(p.value)
        p = p.next
        i = i + 1
    return shown


# history = the actions done, undo_stack = the actions undone that can be redone
class ActivityHistory:
    def __init__(self):
        self.history = ActivityStack()
        self.undo_stack = ActivityStack()


# the opposite of each type of activity
opposite = {"like": "unlike", "comment": "delete comment", "share": "unshare", "follow": "unfollow"}


def revert(activity):
    # "like photo" becomes "unlike photo"
    words = activity.split(" ", 1)
    return opposite[words[0]] + " " + words[1]


# in our code doing the action again only means writing it
def apply(activity):
    return activity


def do_activity(H, activity):
    push(H.history, activity)
    # after a new action the old undone actions can not be redone anymore
    H.undo_stack = ActivityStack()


def undo_last(H):
    activity = pop(H.history)
    if activity is not None:
        print("   undo:", revert(activity))
        push(H.undo_stack, activity)
    return activity


def redo(H):
    activity = pop(H.undo_stack)
    if activity is not None:
        print("   redo:", apply(activity))
        push(H.history, activity)
    return activity


# PART B - NOTIFICATION QUEUE

class NotificationQueue:
    def __init__(self):
        self.head = None
        self.rear = None
        self.count = 0


def enqueue(Q, notification):
    node = Node(notification)
    node.next = None
    if Q.rear is None:
        # empty queue
        Q.head = node
    else:
        Q.rear.next = node
    Q.rear = node
    Q.count = Q.count + 1


def dequeue(Q):
    notification = None
    if Q.head is not None:
        notification = Q.head.value
        Q.head = Q.head.next
        if Q.head is None:
            # the queue is empty now
            Q.rear = None
        Q.count = Q.count - 1
    return notification


def front(Q):
    if Q.head is None:
        return None
    return Q.head.value


# in Python two functions can not have the same name,
# so is_empty and size of the queue are called queue_is_empty and queue_size
def queue_is_empty(Q):
    return Q.head is None


def queue_size(Q):
    return Q.count


def display_pending(Q):
    shown = []
    p = Q.head
    while p is not None:
        print("  ", p.value)
        shown.append(p.value)
        p = p.next
    return shown


# the urgent notification goes at the front, so it is the next one to be processed
def priority_enqueue(Q, notification):
    node = Node(notification)
    node.next = Q.head
    Q.head = node
    if Q.rear is None:
        # the queue was empty, so the new node is also the last one
        Q.rear = node
    Q.count = Q.count + 1


# PART C - INTEGRATED FEED PROCESSING

class FeedProcessor:
    def __init__(self):
        self.recent_activities = ActivityStack()
        self.notification_queue = NotificationQueue()
        self.processed_log = NotificationQueue()


def process_incoming(F):
    if F.notification_queue.head is not None:
        # the oldest notification goes on top of the recent stack
        push(F.recent_activities, dequeue(F.notification_queue))


def batch_process(F, k):
    i = 0
    # stop after k notifications or when the queue is empty
    while i < k and F.notification_queue.head is not None:
        process_incoming(F)
        i = i + 1


def clear_history(F):
    # the most recent activity goes first in the log
    while F.recent_activities.top is not None:
        enqueue(F.processed_log, pop(F.recent_activities))


def get_stats(F):
    return (F.recent_activities.count, F.notification_queue.count, F.processed_log.count)


def stack_values(S):
    values = []
    p = S.top
    while p is not None:
        values.append(p.value)
        p = p.next
    return values


def queue_values(Q):
    values = []
    p = Q.head
    while p is not None:
        values.append(p.value)
        p = p.next
    return values


def check(name, result, expected):
    if result == expected:
        print("OK", name, "->", result)
    else:
        print("FAIL", name, "->", result, "but expected", expected)


def run_tests():
    print("Part A - stack")
    S = ActivityStack()
    check("pop on an empty stack", pop(S), None)
    check("peek on an empty stack", peek(S), None)
    push(S, "like photo of Marco")
    push(S, "comment post of Giulia")
    push(S, "share video of Luca")
    check("peek", peek(S), "share video of Luca")
    check("size", size(S), 3)
    check("display_recent(2)", display_recent(S, 2), ["share video of Luca", "comment post of Giulia"])
    check("display_recent(10), more than the stack", len(display_recent(S, 10)), 3)
    check("pop gives the last one", pop(S), "share video of Luca")
    pop(S)
    pop(S)
    check("stack empty again", (is_empty(S), size(S)), (True, 0))

    print("\nPart A - undo and redo")
    H = ActivityHistory()
    check("undo with no activity", undo_last(H), None)
    do_activity(H, "like photo of Marco")
    do_activity(H, "follow Giulia")
    check("revert of a like", revert("like photo of Marco"), "unlike photo of Marco")
    check("undo_last", undo_last(H), "follow Giulia")
    check("history after undo", stack_values(H.history), ["like photo of Marco"])
    check("redo", redo(H), "follow Giulia")
    check("history after redo", stack_values(H.history), ["follow Giulia", "like photo of Marco"])
    check("redo with nothing to redo", redo(H), None)
    undo_last(H)
    do_activity(H, "share video of Luca")
    # the new action removes the undone actions
    check("redo after a new action", redo(H), None)

    print("\nPart B - queue")
    Q = NotificationQueue()
    check("dequeue on an empty queue", dequeue(Q), None)
    check("front on an empty queue", front(Q), None)
    enqueue(Q, "New follower")
    enqueue(Q, "New like")
    enqueue(Q, "New comment")
    check("display_pending", display_pending(Q), ["New follower", "New like", "New comment"])
    check("dequeue gives the oldest", dequeue(Q), "New follower")
    dequeue(Q)
    dequeue(Q)
    check("queue empty again", (queue_is_empty(Q), queue_size(Q), Q.rear), (True, 0, None))
    # after the queue was emptied, enqueue must still work
    enqueue(Q, "New message")
    check("enqueue after the queue was emptied", queue_values(Q), ["New message"])

    print("\nPart B - priority_enqueue")
    Q = NotificationQueue()
    priority_enqueue(Q, "Password changed")
    check("priority_enqueue on an empty queue", (Q.head.value, Q.rear.value), ("Password changed", "Password changed"))
    enqueue(Q, "New like")
    priority_enqueue(Q, "Login from a new device")
    check("urgent goes first", queue_values(Q), ["Login from a new device", "Password changed", "New like"])
    # enqueue still goes after the last one
    enqueue(Q, "New comment")
    check("enqueue after priority_enqueue", queue_values(Q),
          ["Login from a new device", "Password changed", "New like", "New comment"])
    check("size", queue_size(Q), 4)

    print("\nPart C - feed processor (example of the lab)")
    F = FeedProcessor()
    push(F.recent_activities, "Liked video")
    push(F.recent_activities, "Commented on post")
    push(F.recent_activities, "Shared photo")
    enqueue(F.notification_queue, "New follower")
    enqueue(F.notification_queue, "New like")
    enqueue(F.notification_queue, "New comment")
    process_incoming(F)
    check("recent stack", stack_values(F.recent_activities),
          ["New follower", "Shared photo", "Commented on post", "Liked video"])
    check("notification queue", queue_values(F.notification_queue), ["New like", "New comment"])
    # only 2 notifications are left
    batch_process(F, 5)
    check("batch_process(5) with 2 notifications", get_stats(F), (6, 0, 0))
    clear_history(F)
    check("processed log after clear_history", queue_values(F.processed_log),
          ["New comment", "New like", "New follower", "Shared photo", "Commented on post", "Liked video"])
    check("get_stats after clear_history", get_stats(F), (0, 0, 6))
    process_incoming(F)
    check("process_incoming with an empty queue", get_stats(F), (0, 0, 6))


if __name__ == "__main__":
    run_tests()
