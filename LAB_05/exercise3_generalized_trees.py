# Exercise 3 - Generalized Trees (N-ary Trees) and Representations
# None is used as the NULL pointer of the pseudo-code.
# The binary tree uses the same CategoryNode of exercise 1.

from collections import deque


class GeneralizedCategoryNode:
    def __init__(self, category_id, name, post_count):
        self.category_id = category_id
        self.name = name
        self.post_count = post_count
        self.children = []
        self.parent = None


class CategoryNode:
    def __init__(self, category_id, name, post_count):
        self.category_id = category_id
        self.name = name
        self.post_count = post_count
        self.left = None
        self.right = None
        self.parent = None


def add_child(parent, child):
    parent.children.append(child)
    child.parent = parent


# PART A - BINARY TREE TO GENERALIZED TREE
# as the lab says, the left and the right child both become children

def binary_to_generalized(b):
    if b is None:
        return None
    g = GeneralizedCategoryNode(b.category_id, b.name, b.post_count)
    for child in [b.left, b.right]:
        if child is not None:
            c = binary_to_generalized(child)
            add_child(g, c)
    return g


# PART B - GENERALIZED TREE TO BINARY TREE
# first child, next sibling: left = first child, right = next sibling

def generalized_to_binary(g):
    if g is None:
        return None
    b = CategoryNode(g.category_id, g.name, g.post_count)
    previous = None
    for child in g.children:
        c = generalized_to_binary(child)
        if previous is None:
            # first child
            b.left = c
            c.parent = b
        else:
            # next sibling of the previous child
            previous.right = c
            c.parent = previous
        previous = c
    return b


# TRAVERSALS

def pre_order_generalized(node):
    names = []
    pre_order_add(node, names)
    return names


def pre_order_add(node, names):
    if node is not None:
        names.append(node.name)
        for child in node.children:
            pre_order_add(child, names)


def post_order_generalized(node):
    names = []
    post_order_add(node, names)
    return names


def post_order_add(node, names):
    if node is not None:
        for child in node.children:
            post_order_add(child, names)
        names.append(node.name)


def level_order_generalized(node):
    names = []
    queue = deque()
    if node is not None:
        queue.append(node)
    while len(queue) > 0:
        x = queue.popleft()
        names.append(x.name)
        for child in x.children:
            queue.append(child)
    return names


# maximum number of children of a category
def calculate_fan_out(node):
    fan_out = 0
    if node is not None:
        fan_out = len(node.children)
        for child in node.children:
            f = calculate_fan_out(child)
            if f > fan_out:
                fan_out = f
    return fan_out


# METRICS

def calculate_height_generalized(node):
    if node is None:
        return -1
    height = 0
    for child in node.children:
        h = 1 + calculate_height_generalized(child)
        if h > height:
            height = h
    return height


def count_nodes_generalized(node):
    if node is None:
        return 0
    total = 1
    for child in node.children:
        total = total + count_nodes_generalized(child)
    return total


def count_leaves_generalized(node):
    if node is None:
        return 0
    if len(node.children) == 0:
        return 1
    leaves = 0
    for child in node.children:
        leaves = leaves + count_leaves_generalized(child)
    return leaves


# average number of children of the categories that are not leaves
def calculate_branching_factor(node):
    children, internal = count_children(node)
    factor = 0
    if internal > 0:
        factor = children / internal
    return factor


# returns (number of children, number of categories with children)
def count_children(node):
    if node is None:
        return 0, 0
    children = len(node.children)
    internal = 0
    if children > 0:
        internal = 1
    for child in node.children:
        c, i = count_children(child)
        children = children + c
        internal = internal + i
    return children, internal


def binary_pre_order(b):
    # used to compare the two representations
    names = []
    if b is not None:
        names.append(b.name)
        for x in binary_pre_order(b.left):
            names.append(x)
        for x in binary_pre_order(b.right):
            names.append(x)
    return names


def lab_generalized_tree():
    # the tree of the lab example, with the category Business (the lab gives no post counts for it)
    g = {}
    data = [(1, "Technology", 150), (2, "Programming", 85), (3, "Design", 65), (4, "Business", 40),
            (5, "Python", 42), (6, "Java", 30), (7, "UI/UX", 38), (8, "Graphics", 22),
            (9, "Finance", 20), (10, "Marketing", 15), (11, "HR", 10), (12, "Django", 18), (13, "Flask", 12)]
    for category_id, name, posts in data:
        g[name] = GeneralizedCategoryNode(category_id, name, posts)
    links = [("Technology", "Programming"), ("Technology", "Design"), ("Technology", "Business"),
             ("Programming", "Python"), ("Programming", "Java"), ("Python", "Django"), ("Python", "Flask"),
             ("Design", "UI/UX"), ("Design", "Graphics"),
             ("Business", "Finance"), ("Business", "Marketing"), ("Business", "HR")]
    for parent, child in links:
        add_child(g[parent], g[child])
    return g["Technology"]


def lab_binary_tree():
    # the binary tree of exercise 1
    n = {}
    for category_id, name, posts in [(1, "Technology", 150), (2, "Programming", 85), (3, "Design", 65),
                                      (4, "Python", 42), (5, "Java", 30), (6, "UI/UX", 38),
                                      (7, "Graphics", 22), (8, "Django", 18), (9, "Flask", 12)]:
        n[name] = CategoryNode(category_id, name, posts)
    for parent, left, right in [("Technology", "Programming", "Design"), ("Programming", "Python", "Java"),
                                ("Design", "UI/UX", "Graphics"), ("Python", "Django", "Flask")]:
        n[parent].left = n[left]
        n[parent].right = n[right]
        n[left].parent = n[parent]
        n[right].parent = n[parent]
    return n["Technology"]


def chain(n):
    # every category has only one child
    first = GeneralizedCategoryNode(0, "level 0", 0)
    c = first
    for i in range(1, n):
        x = GeneralizedCategoryNode(i, "level " + str(i), 0)
        add_child(c, x)
        c = x
    return first


def check(name, result, expected):
    if result == expected:
        print("OK", name, "->", result)
    else:
        print("FAIL", name, "->", result, "but expected", expected)


def run_tests():
    print("Example of the lab (generalized tree)")
    g = lab_generalized_tree()
    check("pre_order_generalized", pre_order_generalized(g),
          ["Technology", "Programming", "Python", "Django", "Flask", "Java", "Design", "UI/UX", "Graphics",
           "Business", "Finance", "Marketing", "HR"])
    check("post_order_generalized", post_order_generalized(g),
          ["Django", "Flask", "Python", "Java", "Programming", "UI/UX", "Graphics", "Design",
           "Finance", "Marketing", "HR", "Business", "Technology"])
    check("level_order_generalized", level_order_generalized(g),
          ["Technology", "Programming", "Design", "Business", "Python", "Java", "UI/UX", "Graphics",
           "Finance", "Marketing", "HR", "Django", "Flask"])
    check("calculate_fan_out", calculate_fan_out(g), 3)
    check("calculate_height_generalized", calculate_height_generalized(g), 3)
    check("count_nodes_generalized", count_nodes_generalized(g), 13)
    check("count_leaves_generalized", count_leaves_generalized(g), 8)
    # 5 categories have children: (3 + 2 + 2 + 2 + 3) / 5, the lab forgets Python and gets 2.5
    check("calculate_branching_factor", calculate_branching_factor(g), 2.4)

    print("\nConversions")
    b = generalized_to_binary(g)
    check("first child, next sibling: Technology.left, Technology.right", (b.left.name, b.right), ("Programming", None))
    check("Programming.right = Design, Design.right = Business", (b.left.right.name, b.left.right.right.name), ("Design", "Business"))
    check("parent of Design (binary) = Programming", b.left.right.parent.name, "Programming")
    check("binary pre-order = generalized pre-order", binary_pre_order(b), pre_order_generalized(g))
    t = lab_binary_tree()
    g2 = binary_to_generalized(t)
    check("binary_to_generalized: children of Technology", [g2.children[0].name, g2.children[1].name], ["Programming", "Design"])
    check("binary_to_generalized: 9 categories, height 3", (count_nodes_generalized(g2), calculate_height_generalized(g2)), (9, 3))
    # the two conversions are not inverse: right means "child" in one and "sibling" in the other
    back = binary_to_generalized(generalized_to_binary(g))
    check("round trip: same 13 categories", count_nodes_generalized(back), 13)
    check("round trip: height 6 instead of 3", calculate_height_generalized(back), 6)

    print("\nEdge cases")
    check("empty tree: conversions", (binary_to_generalized(None), generalized_to_binary(None)), (None, None))
    check("empty tree: traversals", (pre_order_generalized(None), level_order_generalized(None)), ([], []))
    check("empty tree: height, nodes, leaves, fan-out", (calculate_height_generalized(None), count_nodes_generalized(None),
          count_leaves_generalized(None), calculate_fan_out(None)), (-1, 0, 0, 0))
    one = GeneralizedCategoryNode(1, "Sport", 10)
    check("single category: height, leaves, branching factor", (calculate_height_generalized(one),
          count_leaves_generalized(one), calculate_branching_factor(one)), (0, 1, 0))
    star = GeneralizedCategoryNode(0, "Food", 5)
    for i in range(1, 6):
        add_child(star, GeneralizedCategoryNode(i, "food " + str(i), 1))
    check("one category with 5 children: fan-out, branching factor", (calculate_fan_out(star), calculate_branching_factor(star)), (5, 5))
    bs = generalized_to_binary(star)
    check("5 children in binary: one left, then a chain of 4 right", (calculate_height_generalized(binary_to_generalized(bs)), bs.left.name), (5, "food 1"))

    print("\nVery deep hierarchy (2000 levels)")
    deep = chain(2000)
    crashed = False
    try:
        calculate_height_generalized(deep)
    except RecursionError:
        crashed = True
    check("recursive height crashes", crashed, True)
    check("level order (queue) still works", len(level_order_generalized(deep)), 2000)


if __name__ == "__main__":
    run_tests()
