from utility import load_csv

"""
Building/Traversing Graphs/Trees from scratch.

This is me messing around without much background reading on the subject to get a rough idea of whats going on.
"""

class Node:

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.level = 0
        self.is_root = False
        self.is_parent = False

    def __str__(self):
        return "{}:{}:{}".format(self.name, self.parent, self.level)

class Tree:

    def __init__(self):
        self.nodes = []
        self.nodes_dict = {}  # Not used atm

    @staticmethod
    def from_nodes_csv(file_path):
        obj = Tree()
        data = load_csv(file_path)[1:]
        for v in data:
            node = Node(v[0], v[1])
            obj.attach_node(node)

        return obj

    def attach_node(self, node):
        """
        Doc Doc Doc
        """
        assert type(node) == Node, "node arg must be of type Node"

        # First Node is by default the root node
        if not self.nodes:
            node.parent = None
            node.level = 0
            node.is_root = True
            self.nodes.append(node)
            return

        # Make sure Node is attaching to a valid parent
        assert node.parent in self.get_node_names(), "N:{}P:{} Invalid Parent".format(node.name, node.parent)

        # Get level of the Parent. Level of node is that -1
        parent_level = [n.level for n in self.nodes if n.name == node.parent][0]
        node.level = parent_level + 1

        # Set the parent node is_parent to True (might already be)
        for n in self.nodes:
            if n.name == node.parent:
                n.is_parent = True
                break

        self.nodes.append(node)

    def get_node_names(self):
        return [n.name for n in self.nodes]

    def get_node_children(self, name):
        # Get Immediate Children
        child_nodes = [n for n in self.nodes if n.parent == name]

        # Search


        return child_nodes




    def __str__(self):
        return " ".join([str(n) for n in self.nodes])





if __name__ == "__main__":

    test_tree = Tree.from_nodes_csv("scratch_nodes.csv")

    print(test_tree)

    print(test_tree.get_node_children("b"))