# Exercise 1 - Content Feed Navigation with Doubly Linked List
# The feed of stories is a doubly linked list: every node has a pointer next and a pointer prev.
# None is used as the NULL pointer of the pseudo-code.


class StoryNode:
    def __init__(self, story_id, user_id, content_preview, timestamp):
        self.story_id = story_id
        self.user_id = user_id
        self.content_preview = content_preview
        self.timestamp = timestamp
        self.views = 0
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None
        self.size = 0


def add_story(L, node):
    node.prev = L.tail
    node.next = None
    if L.tail is None:
        # empty feed: the new story is also the first one and the current one
        L.head = node
        L.current = node
    else:
        L.tail.next = node
    L.tail = node
    L.size = L.size + 1


def find(L, story_id):
    p = L.head
    while p is not None and p.story_id != story_id:
        p = p.next
    # None if the story is not in the feed
    return p


# p must be a node of L
def unlink(L, p):
    if p.prev is None:
        L.head = p.next
    else:
        p.prev.next = p.next
    if p.next is None:
        L.tail = p.prev
    else:
        p.next.prev = p.prev
    p.next = None
    p.prev = None
    L.size = L.size - 1


def remove_story(L, story_id):
    removed = False
    p = find(L, story_id)
    if p is not None:
        # if we remove the current story, current goes to the next one (or to the previous one at the end)
        if L.current is p:
            if p.next is not None:
                L.current = p.next
            else:
                L.current = p.prev
        unlink(L, p)
        removed = True
    return removed


def move_forward(L):
    # no next story
    if L.current is None or L.current.next is None:
        return None
    L.current = L.current.next
    return L.current


def move_backward(L):
    # no previous story
    if L.current is None or L.current.prev is None:
        return None
    L.current = L.current.prev
    return L.current


def jump_to(L, story_id):
    p = find(L, story_id)
    # current does not change if the story is not found
    if p is not None:
        L.current = p
    return p


def insert_after(L, current_id, new_story):
    inserted = False
    p = find(L, current_id)
    if p is not None:
        new_story.prev = p
        new_story.next = p.next
        if p.next is None:
            # p was the last story
            L.tail = new_story
        else:
            p.next.prev = new_story
        p.next = new_story
        L.size = L.size + 1
        inserted = True
    return inserted


def display_around_current(L, k):
    # the ids of the shown stories are also returned, so the tests can check them
    shown = []
    if L.current is not None:
        # go back k stories, or stop at the first one
        start = L.current
        before = 0
        while before < k and start.prev is not None:
            start = start.prev
            before = before + 1
        # show the stories before, the current one and k stories after (or stop at the last one)
        p = start
        count = 0
        while p is not None and count < before + 1 + k:
            print("  ", p.story_id, p.content_preview)
            shown.append(p.story_id)
            p = p.next
            count = count + 1
    return shown


def track_view(L):
    if L.current is not None:
        L.current.views = L.current.views + 1


def most_viewed(L):
    best = L.head
    p = L.head
    while p is not None:
        if p.views > best.views:
            best = p
        p = p.next
    return best


# each time we take the most viewed story of the old list and we add it at the end of a new list
def reorder_by_views(L):
    # we keep the same current story
    cur = L.current
    N = DoublyLinkedList()
    while L.head is not None:
        best = most_viewed(L)
        unlink(L, best)
        add_story(N, best)
    L.head = N.head
    L.tail = N.tail
    L.size = N.size
    L.current = cur


def ids_forward(L):
    ids = []
    p = L.head
    while p is not None:
        ids.append(p.story_id)
        p = p.next
    return ids


def ids_backward(L):
    ids = []
    p = L.tail
    while p is not None:
        ids.append(p.story_id)
        p = p.prev
    return ids


def make_feed(stories):
    L = DoublyLinkedList()
    for story_id, text in stories:
        add_story(L, StoryNode(story_id, 100 + story_id, text, story_id))
    return L


def check(name, result, expected):
    if result == expected:
        print("OK", name, "->", result)
    else:
        print("FAIL", name, "->", result, "but expected", expected)


def check_links(name, L):
    # the list read backwards must be the same list read forwards, and size must be right
    forward = ids_forward(L)
    backward = ids_backward(L)
    backward.reverse()
    check(name + " (links and size)", forward == backward and len(forward) == L.size, True)


def run_tests():
    print("Example of the lab")
    L = make_feed([(1, "Morning coffee"), (2, "Workout complete"), (3, "Sunset photo")])
    # Story2 is viewed two times and Story3 one time
    jump_to(L, 2)
    track_view(L)
    track_view(L)
    move_forward(L)
    track_view(L)
    check("most viewed", most_viewed(L).story_id, 2)
    reorder_by_views(L)
    check("after reorder_by_views", ids_forward(L), [2, 3, 1])
    check_links("after reorder_by_views", L)
    check("current does not change", L.current.story_id, 3)

    print("\nNavigation")
    L = make_feed([(1, "Pizza a Napoli"), (2, "Gelato a Roma"), (3, "Duomo di Milano")])
    check("current of a new feed", L.current.story_id, 1)
    check("move_backward at the first story", move_backward(L), None)
    move_forward(L)
    move_forward(L)
    check("move_forward to the last story", L.current.story_id, 3)
    check("move_forward at the last story", move_forward(L), None)
    check("current stays on the last story", L.current.story_id, 3)
    check("move_backward", move_backward(L).story_id, 2)
    check("jump_to a story that does not exist", jump_to(L, 9), None)
    check("current does not change", L.current.story_id, 2)

    print("\nInsert and remove")
    check("insert_after a story that does not exist", insert_after(L, 9, StoryNode(4, 104, "Ponte di Rialto", 4)), False)
    insert_after(L, 3, StoryNode(4, 104, "Ponte di Rialto", 4))
    check("insert_after the last story", ids_forward(L), [1, 2, 3, 4])
    check("tail after insert_after", L.tail.story_id, 4)
    insert_after(L, 1, StoryNode(5, 105, "Torre di Pisa", 5))
    check("insert_after in the middle", ids_forward(L), [1, 5, 2, 3, 4])
    check_links("after insert_after", L)
    check("remove a story that does not exist", remove_story(L, 9), False)
    # current is story 2, in the middle
    remove_story(L, 2)
    check("remove the current story", L.current.story_id, 3)
    jump_to(L, 4)
    remove_story(L, 4)
    check("remove the current story at the end", L.current.story_id, 3)
    remove_story(L, 1)
    check("remove the first story", ids_forward(L), [5, 3])
    check_links("after remove_story", L)

    print("\nDisplay around current")
    L = make_feed([(1, "a"), (2, "b"), (3, "c"), (4, "d"), (5, "e"), (6, "f"), (7, "g")])
    # (current story, k, expected stories)
    tests = [
        # in the middle
        (4, 2, [2, 3, 4, 5, 6]),
        # near the start, only one story before
        (2, 3, [1, 2, 3, 4, 5]),
        # only the current story
        (2, 0, [2]),
        # k bigger than the feed
        (2, 10, [1, 2, 3, 4, 5, 6, 7]),
    ]
    for current, k, expected in tests:
        jump_to(L, current)
        check("current " + str(current) + ", k = " + str(k), display_around_current(L, k), expected)

    print("\nEmpty feed and single story")
    E = DoublyLinkedList()
    check("move_forward on an empty feed", move_forward(E), None)
    check("most_viewed on an empty feed", most_viewed(E), None)
    check("display on an empty feed", display_around_current(E, 2), [])
    reorder_by_views(E)
    check("reorder an empty feed", ids_forward(E), [])
    add_story(E, StoryNode(1, 101, "Ciao", 1))
    remove_story(E, 1)
    check("remove the only story", (E.head, E.tail, E.current, E.size), (None, None, None, 0))

    print("\nReorder with equal views")
    L = make_feed([(1, "a"), (2, "b"), (3, "c"), (4, "d"), (5, "e")])
    views = {1: 3, 2: 1, 3: 3, 4: 0, 5: 1}
    for story_id in views:
        jump_to(L, story_id)
        for k in range(views[story_id]):
            track_view(L)
    reorder_by_views(L)
    # equal views keep the chronological order
    check("reorder with equal views", ids_forward(L), [1, 3, 2, 5, 4])
    check_links("after reorder", L)


if __name__ == "__main__":
    run_tests()
