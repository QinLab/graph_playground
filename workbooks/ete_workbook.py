from ete3 import Tree

"""
Various things related to the ete3 package.

Of interest:
Short-leaf branch
Longest-leaf branch
"""

def print_random_tree(num_nodes=5):
    """
    Doc Doc Doc
    """

    t = Tree()
    t.populate(num_nodes)

    print("t", t)
    print("children", t.children)
    print("get_children", t.get_children())
    print("up", t.up)
    print("name", t.name)
    print("dist", t.dist)
    print("is_leaf", t.is_leaf())
    print("get_tree_root", t.get_tree_root())
    print("children[0].get_tree_root", t.children[0].get_tree_root())
    print("children[0].children[0].get_tree_root", t.children[0].children[0].get_tree_root())
    for leaf in t:
        print(leaf.name)

if __name__ == "__main__":

    print_random_tree()
