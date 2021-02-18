
"""
Newer iteration of graph.py which will probably be removed eventually, more focused on working with YoloCSV and some
assumptions we are able to make regarding the raw data there. These assumptions may simply things, as we are working
with a directed Tree rather than an undirected Graph.

graph_dict in init is the result of YoloCSV.to_graph_dict()
"""


class YoloTree:


    def __init__(self, graph_dict):
        self.graph_dict = graph_dict
        self.tree_dict = {}
        self.tree_info = {}
        self._on_init()

    def _on_init(self):
        """
        Root function for initialization.
        """

        # Currently we assume parent node(s) are the cells that share the same initial time-step.
        # Main branch will start from these. Possible multiple, but haven't tried that yet. Trap 4?
        root_nodes = [k for k in self.graph_dict if k.split(".", 1)[0] == "1"]
        self.tree_info["root_nodes"] = root_nodes
        self.tree_info["branch_edges"] = []

        self._populate_tree_dict()

    def _populate_tree_dict(self):
        """
        Doc Doc Doc
        """

        branch_nodes = list(self.tree_info["root_nodes"])

        for node in self.graph_dict:

            # Add root node(s) to tree dict.
            if node in self.tree_info["root_nodes"]:
                self.tree_dict[node] = []
                continue

            # Get edges for node
            edges = list(self.graph_dict[node])

            # Check if edge to a root or branch node. Add to that node's branch and remove.
            for edge in edges:
                if edge in branch_nodes:
                    self.tree_dict[edge].append(node)
                    edges.remove(edge)
                    continue
                # Attempt to add node to appropriate root node.
                for branch_node in branch_nodes:
                    last_branch_edges = self.tree_dict[branch_node]
                    if not last_branch_edges:
                        continue
                    if last_branch_edges[-1] == edge:
                        self.tree_dict[branch_node].append(node)
                        edges.remove(edge)


            # Check remaining nodes for change in predecessorID. This indicates a branch may have formed here.
            for edge in edges:
                if edge.split(".", 1)[-1] != node.split(".", 1)[-1]:
                    # Change + difference in time means we need to track a new branch.
                    if int(edge.split(".", 1)[0]) > int(node.split(".", 1)[0]):
                        self.tree_dict[edge] = []
                        self.tree_info["branch_edges"].append([node, edge])
                        branch_nodes.append(edge)













