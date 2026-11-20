# Exercise 1 - Binary Tree Representation of Content Categories
# None is used as the NULL pointer of the pseudo-code.
# As in the lecture, the height of a node is the number of edges from the root,
# and the height of the empty tree is -1 (so a single category has height 0).

from collections import deque


class CategoryNode:
    def __init__(self, category_id, name, post_count):
        self.category_id = category_id
        self.name = name
        self.post_count = post_count
        self.left = None
        self.right = None
        self.parent = None


def add_children(node, left, right):
    # links the two children to the node, also with the parent pointers
    node.left = left
    node.right = right
    if left is not None:
        left.parent = node
    if right is not None:
        right.parent = node


# 1 - TREE METRICS

def calculate_height(node):
    height = -1
    if node is not None:
        hl = calculate_height(node.left)
        hr = calculate_height(node.right)
        height = 1 + max(hl, hr)
    return height


# number of edges from node to the target, -1 if the target is not in the tree
def calculate_node_height(node, target_id):
    if node is None:
        return -1
    if node.category_id == target_id:
        return 0
    h = calculate_node_height(node.left, target_id)
    if h == -1:
        h = calculate_node_height(node.right, target_id)
    if h != -1:
        # the target is under this node, so one edge more
        h = h + 1
    return h


def count_nodes(node):
    total = 0
    if node is not None:
        total = 1 + count_nodes(node.left) + count_nodes(node.right)
    return total


def count_leaves(node):
    if node is None:
        return 0
    if node.left is None and node.right is None:
        return 1
    return count_leaves(node.left) + count_leaves(node.right)


def is_balanced(node):
    if node is None:
        return True
    diff = calculate_height(node.left) - calculate_height(node.right)
    if diff > 1 or diff < -1:
        return False
    return is_balanced(node.left) and is_balanced(node.right)


# 2 - TREE PROPERTIES (definitions of the lecture, slides 25-26)

def has_0_or_2_children(node):
    if node is None:
        return True
    if (node.left is None) != (node.right is None):
        # only one child
        return False
    return has_0_or_2_children(node.left) and has_0_or_2_children(node.right)


# full: every node has 0 or 2 children, and the tree is balanced
def is_full_binary_tree(node):
    return has_0_or_2_children(node) and is_balanced(node)


# complete: all the levels are full, so there are 2^(H+1) - 1 nodes
def is_complete_binary_tree(node):
    h = calculate_height(node)
    return count_nodes(node) == 2 ** (h + 1) - 1


# perfect: all the levels are full except the last one, filled from the left
def is_perfect_binary_tree(node):
    if node is None:
        return True
    queue = deque()
    queue.append(node)
    missing = False      # True after the first missing child
    ok = True
    while ok and len(queue) > 0:
        x = queue.popleft()
        for child in [x.left, x.right]:
            if child is None:
                missing = True
            elif missing:
                # a node after a hole
                ok = False
            else:
                queue.append(child)
    return ok


# 3 - SEARCH AND NAVIGATION

def find_category(category_id, node):
    if node is None or node.category_id == category_id:
        return node
    found = find_category(category_id, node.left)
    if found is None:
        found = find_category(category_id, node.right)
    return found


def find_path_to_root(category_id, node):
    # find the category, then go up with the parent pointers
    path = []
    x = find_category(category_id, node)
    while x is not None:
        path.append(x.name)
        x = x.parent
    return path


# both categories must be in the tree
def lowest_common_ancestor(id1, id2, node):
    if node is None:
        return None
    if node.category_id == id1 or node.category_id == id2:
        return node
    a = lowest_common_ancestor(id1, id2, node.left)
    b = lowest_common_ancestor(id1, id2, node.right)
    if a is not None and b is not None:
        # one category on each side
        return node
    if a is not None:
        return a
    return b


def lab_tree():
    # the example of the lab: 9 categories, ids from 1 to 9
    technology = CategoryNode(1, "Technology", 150)
    programming = CategoryNode(2, "Programming", 85)
    design = CategoryNode(3, "Design", 65)
    python = CategoryNode(4, "Python", 42)
    java = CategoryNode(5, "Java", 30)
    ui_ux = CategoryNode(6, "UI/UX", 38)
    graphics = CategoryNode(7, "Graphics", 22)
    django = CategoryNode(8, "Django", 18)
    flask = CategoryNode(9, "Flask", 12)
    add_children(technology, programming, design)
    add_children(programming, python, java)
    add_children(design, ui_ux, graphics)
    add_children(python, django, flask)
    return technology


def chain(n):
    # a skewed tree: every category has only a left child
    first = CategoryNode(0, "level 0", 0)
    c = first
    for i in range(1, n):
        x = CategoryNode(i, "level " + str(i), 0)
        add_children(c, x, None)
        c = x
    return first


def complete_tree():
    # 7 categories, all the levels are full
    nodes = []
    for i in range(7):
        nodes.append(CategoryNode(i, "c" + str(i), 1))
    add_children(nodes[0], nodes[1], nodes[2])
    add_children(nodes[1], nodes[3], nodes[4])
    add_children(nodes[2], nodes[5], nodes[6])
    return nodes[0]


def check(name, result, expected):
    if result == expected:
        print("OK", name, "->", result)
    else:
        print("FAIL", name, "->", result, "but expected", expected)


def run_tests():
    print("Example of the lab")
    t = lab_tree()
    check("calculate_height", calculate_height(t), 3)
    check("calculate_node_height(Java)", calculate_node_height(t, 5), 2)
    check("calculate_node_height(Django)", calculate_node_height(t, 8), 3)
    check("count_nodes (the lab says 7, the tree has 9)", count_nodes(t), 9)
    check("count_leaves", count_leaves(t), 5)
    check("is_balanced", is_balanced(t), True)
    check("is_full_binary_tree", is_full_binary_tree(t), True)
    check("is_complete_binary_tree", is_complete_binary_tree(t), False)
    check("is_perfect_binary_tree", is_perfect_binary_tree(t), True)
    check("find_category(Python)", find_category(4, t).name, "Python")
    check("find_path_to_root(Django)", find_path_to_root(8, t), ["Django", "Python", "Programming", "Technology"])
    check("lowest_common_ancestor(Django, Java)", lowest_common_ancestor(8, 5, t).name, "Programming")
    check("lowest_common_ancestor(Django, Flask)", lowest_common_ancestor(8, 9, t).name, "Python")
    check("lowest_common_ancestor(Django, Graphics)", lowest_common_ancestor(8, 7, t).name, "Technology")
    check("lowest_common_ancestor(Python, Django)", lowest_common_ancestor(4, 8, t).name, "Python")

    print("\nEdge cases")
    check("empty tree: height, nodes, leaves", (calculate_height(None), count_nodes(None), count_leaves(None)), (-1, 0, 0))
    check("empty tree: balanced, full, complete, perfect",
          (is_balanced(None), is_full_binary_tree(None), is_complete_binary_tree(None), is_perfect_binary_tree(None)),
          (True, True, True, True))
    one = CategoryNode(1, "Sport", 10)
    check("single category: height, leaves", (calculate_height(one), count_leaves(one)), (0, 1))
    check("single category: full, complete, perfect",
          (is_full_binary_tree(one), is_complete_binary_tree(one), is_perfect_binary_tree(one)), (True, True, True))
    check("category not in the tree: find", find_category(99, t), None)
    check("category not in the tree: node height", calculate_node_height(t, 99), -1)
    check("category not in the tree: path", find_path_to_root(99, t), [])
    check("path of the root", find_path_to_root(1, t), ["Technology"])
    c = complete_tree()
    check("7 categories, all levels full: complete, perfect", (is_complete_binary_tree(c), is_perfect_binary_tree(c)), (True, True))
    # remove the first child of c1: the hole is not on the right
    c.left.left = None
    check("hole on the left of the last level: perfect", is_perfect_binary_tree(c), False)
    check("hole on the left of the last level: full (c1 has 1 child)", is_full_binary_tree(c), False)
    s = chain(3)
    check("skewed tree of 3: height, balanced", (calculate_height(s), is_balanced(s)), (2, False))
    check("skewed tree of 3: full, perfect", (is_full_binary_tree(s), is_perfect_binary_tree(s)), (False, False))

    print("\nVery deep skewed tree (2000 categories)")
    s = chain(2000)
    crashed = False
    try:
        calculate_height(s)
    except RecursionError:
        crashed = True
    check("recursive calculate_height crashes", crashed, True)


if __name__ == "__main__":
    run_tests()
