# Exercise 2 - Tree Traversals for Content Processing
# The same category tree of exercise 1. None is used as the NULL pointer of the pseudo-code.
# The depth of a category is the number of edges from the root.


class CategoryNode:
    def __init__(self, category_id, name, post_count):
        self.category_id = category_id
        self.name = name
        self.post_count = post_count
        self.left = None
        self.right = None
        self.parent = None


def add_children(node, left, right):
    node.left = left
    node.right = right
    if left is not None:
        left.parent = node
    if right is not None:
        right.parent = node


def label(node):
    # "Technology (150)"
    return node.name + " (" + str(node.post_count) + ")"


# PART A - IN-ORDER (left, root, right)

def in_order_collect(node):
    names = []
    in_order_add(node, names)
    return names


def in_order_add(node, names):
    if node is not None:
        in_order_add(node.left, names)
        names.append(node.name)
        in_order_add(node.right, names)


# list of (name, total of the posts until this category)
def in_order_accumulate_posts(node):
    result = []
    accumulate(node, result)
    return result


def accumulate(node, result):
    if node is not None:
        accumulate(node.left, result)
        total = node.post_count
        if len(result) > 0:
            # add the running total of the previous category
            total = total + result[len(result) - 1][1]
        result.append((node.name, total))
        accumulate(node.right, result)


def in_order_find_kth(k, node):
    # counter[0] = number of categories already visited in in-order
    counter = [0]
    return find_kth(k, node, counter)


def find_kth(k, node, counter):
    found = None
    if node is not None:
        found = find_kth(k, node.left, counter)
        if found is None:
            counter[0] = counter[0] + 1
            if counter[0] == k:
                found = node
            else:
                found = find_kth(k, node.right, counter)
    return found


# PART B - PRE-ORDER (root, left, right)

def pre_order_export(node):
    lines = []
    export_lines(node, 0, lines)
    return "\n".join(lines)


def export_lines(node, level, lines):
    if node is not None:
        # 2 spaces for each level
        lines.append("  " * level + label(node))
        export_lines(node.left, level + 1, lines)
        export_lines(node.right, level + 1, lines)


def pre_order_copy(node):
    if node is None:
        return None
    copy = CategoryNode(node.category_id, node.name, node.post_count)
    left = pre_order_copy(node.left)
    right = pre_order_copy(node.right)
    add_children(copy, left, right)
    return copy


def pre_order_serialize(node):
    labels = []
    serialize(node, labels)
    return " | ".join(labels)


def serialize(node, labels):
    if node is not None:
        labels.append(label(node))
        serialize(node.left, labels)
        serialize(node.right, labels)


# PART C - POST-ORDER (left, right, root)

def post_order_total_posts(node):
    total = 0
    if node is not None:
        left = post_order_total_posts(node.left)
        right = post_order_total_posts(node.right)
        total = left + right + node.post_count
    return total


def post_order_average_depth(node):
    depth_sum, leaves = leaf_depths(node, 0)
    average = 0
    if leaves > 0:
        average = depth_sum / leaves
    return average


# returns (sum of the depths of the leaves, number of leaves)
def leaf_depths(node, depth):
    if node is None:
        return 0, 0
    if node.left is None and node.right is None:
        return depth, 1
    s1, n1 = leaf_depths(node.left, depth + 1)
    s2, n2 = leaf_depths(node.right, depth + 1)
    return s1 + s2, n1 + n2


def post_order_collect_leaves(node):
    leaves = []
    collect_leaves(node, leaves)
    return leaves


def collect_leaves(node, leaves):
    if node is not None:
        collect_leaves(node.left, leaves)
        collect_leaves(node.right, leaves)
        if node.left is None and node.right is None:
            leaves.append(node.name)


# ANALYTICS

# only the posts of the category itself; with equal counts we keep the first one in pre-order
def find_most_popular_category(node):
    best = node
    if node is not None:
        for child in [node.left, node.right]:
            b = find_most_popular_category(child)
            if b is not None and b.post_count > best.post_count:
                best = b
    return best


def number_of_children(node):
    n = 0
    if node.left is not None:
        n = n + 1
    if node.right is not None:
        n = n + 1
    return n


def category_with_most_subcategories(node):
    best = node
    if node is not None:
        for child in [node.left, node.right]:
            b = category_with_most_subcategories(child)
            if b is not None and number_of_children(b) > number_of_children(best):
                best = b
    return best


# number of categories at each depth
def distribution_by_depth(node):
    counts = {}
    count_depths(node, 0, counts)
    return counts


def count_depths(node, depth, counts):
    if node is not None:
        if depth in counts:
            counts[depth] = counts[depth] + 1
        else:
            counts[depth] = 1
        count_depths(node.left, depth + 1, counts)
        count_depths(node.right, depth + 1, counts)


# ITERATIVE VERSIONS WITH AN EXPLICIT STACK (question 3)

def pre_order_iterative(node):
    names = []
    stack = []
    if node is not None:
        stack.append(node)
    while len(stack) > 0:
        x = stack.pop()
        names.append(x.name)
        # right first, so the left child is popped first
        if x.right is not None:
            stack.append(x.right)
        if x.left is not None:
            stack.append(x.left)
    return names


def in_order_iterative(node):
    names = []
    stack = []
    x = node
    while x is not None or len(stack) > 0:
        # go down on the left and keep the categories on the stack
        while x is not None:
            stack.append(x)
            x = x.left
        x = stack.pop()
        names.append(x.name)
        x = x.right
    return names


def lab_tree():
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


def check(name, result, expected):
    if result == expected:
        print("OK", name, "->", result)
    else:
        print("FAIL", name, "->", result, "but expected", expected)


def run_tests():
    print("Example of the lab")
    t = lab_tree()
    in_order = ["Django", "Python", "Flask", "Programming", "Java", "Technology", "UI/UX", "Design", "Graphics"]
    check("in_order_collect", in_order_collect(t), in_order)
    acc = in_order_accumulate_posts(t)
    check("in_order_accumulate_posts: first and last", (acc[0], acc[8]), (("Django", 18), ("Graphics", 462)))
    check("in_order_find_kth(4)", in_order_find_kth(4, t).name, "Programming")
    export = ("Technology (150)\n  Programming (85)\n    Python (42)\n      Django (18)\n      Flask (12)\n"
              "    Java (30)\n  Design (65)\n    UI/UX (38)\n    Graphics (22)")
    check("pre_order_export", pre_order_export(t) == export, True)
    print(pre_order_export(t))
    check("pre_order_serialize", pre_order_serialize(t),
          "Technology (150) | Programming (85) | Python (42) | Django (18) | Flask (12) | "
          "Java (30) | Design (65) | UI/UX (38) | Graphics (22)")
    check("post_order_total_posts(Python)", post_order_total_posts(t.left.left), 72)
    check("post_order_total_posts(Programming)", post_order_total_posts(t.left), 187)
    check("post_order_total_posts(Design)", post_order_total_posts(t.right), 125)
    check("post_order_total_posts(Technology)", post_order_total_posts(t), 462)
    check("post_order_average_depth", post_order_average_depth(t), 2.4)
    check("post_order_collect_leaves", post_order_collect_leaves(t), ["Django", "Flask", "Java", "UI/UX", "Graphics"])
    check("find_most_popular_category", find_most_popular_category(t).name, "Technology")
    # 4 categories have 2 children, we keep the first one in pre-order (the lab says Programming)
    check("category_with_most_subcategories", category_with_most_subcategories(t).name, "Technology")
    check("distribution_by_depth", distribution_by_depth(t), {0: 1, 1: 2, 2: 4, 3: 2})

    print("\nCopy")
    c = pre_order_copy(t)
    check("same serialization", pre_order_serialize(c), pre_order_serialize(t))
    check("different nodes", c is t or c.left is t.left, False)
    c.left.post_count = 0
    check("change the copy, the original does not change", t.left.post_count, 85)
    check("parent pointers of the copy", c.left.left.parent is c.left, True)

    print("\nEdge cases")
    check("empty tree: collect, serialize, export", (in_order_collect(None), pre_order_serialize(None), pre_order_export(None)), ([], "", ""))
    check("empty tree: total, average depth, leaves", (post_order_total_posts(None), post_order_average_depth(None), post_order_collect_leaves(None)), (0, 0, []))
    check("empty tree: copy, most popular", (pre_order_copy(None), find_most_popular_category(None)), (None, None))
    check("k = 1 and k = 9", (in_order_find_kth(1, t).name, in_order_find_kth(9, t).name), ("Django", "Graphics"))
    check("k = 0 and k = 10 (out of range)", (in_order_find_kth(0, t), in_order_find_kth(10, t)), (None, None))
    one = CategoryNode(1, "Sport", 10)
    check("single category: average depth, leaves", (post_order_average_depth(one), post_order_collect_leaves(one)), (0, ["Sport"]))
    check("single category: most subcategories", category_with_most_subcategories(one).name, "Sport")

    print("\nIterative versions")
    check("pre_order_iterative = recursive pre-order", pre_order_iterative(t), ["Technology", "Programming", "Python", "Django", "Flask", "Java", "Design", "UI/UX", "Graphics"])
    check("in_order_iterative = in_order_collect", in_order_iterative(t), in_order)
    s = chain(5000)
    crashed = False
    try:
        in_order_collect(s)
    except RecursionError:
        crashed = True
    check("skewed tree of 5000: recursive in-order crashes", crashed, True)
    check("skewed tree of 5000: iterative in-order works", len(in_order_iterative(s)), 5000)
    check("skewed tree of 5000: iterative pre-order works", len(pre_order_iterative(s)), 5000)


if __name__ == "__main__":
    run_tests()
