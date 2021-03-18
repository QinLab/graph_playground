from anytree import Node, RenderTree
from anytree.exporter import DotExporter

"""
Doc Doc Doc
"""


def run_any_tree(graph_info):

    print(graph_info)

    nodes = list(graph_info["graph"].keys())
    any_node_lu = dict()
    root_node = Node(nodes[0])
    any_node_lu[nodes[0]] = root_node

    for node in nodes[1:]:
        parent_node = graph_info["graph"][node][0]
        print(node, parent_node)
        new_node = Node(node, parent=any_node_lu[parent_node])
        any_node_lu[node] = new_node

    with open("data/any_tree_recent.txt", "w") as w_file:
        for pre, fill, node in RenderTree(root_node):
            w_file.write("%s%s" % (pre, node.name))
    # for pre, fill, node in RenderTree(root_node):
    #     print("%s%s" % (pre, node.name))

    # print(RenderTree(root_node))
    # DotExporter(root_node).to_picture("anytree_recent_query.png")
