

"""
Graph Obj

Currently initialized from a dict w/ following format:
Example:
g = {"a": ["d"],
     "b": ["c", "f"],
     "c": ["b", "c", "d", "e"],
     "d": ["a", "c"],
     "e": ["c"],
     "f": [],
    }
"""


class Graph:


    def __init__(self, graph_dict):
        self.graph_dict = graph_dict
        self.branch_dict = None
        self.info = {}
        self._on_init()

    def _on_init(self):
        """
        Doc Doc Doc
        """

        self._make_branch_dict()
        self._calc_main_branch()
        self._calc_leaf_branch()

    def get_nodes(self):
        """
        Returns the nodes of the graph.
        """
        return list(self.graph_dict)

    def get_edges(self):
        """
        Returns the edges of the graph.
        """
        edges = []
        for node in self.graph_dict:
            for neighbour in self.graph_dict[node]:
                if {node, neighbour} not in edges:
                    edges.append({node, neighbour})
        return edges

    def _make_branch_dict(self, verbose=False):
        """
        Took a couple hours to work through this but looks to be working. Need to clean it up some.

        I found a "correct" implementation and it appears to be similar, so look to be on the right track.
        https://www.geeksforgeeks.org/longest-path-undirected-tree/
        """
        branch_dict = {}

        # Iterate though all the nodes
        for node in self.graph_dict:
            if verbose:
                print("*-------NODE", node)

            branch_dict[node] = {}
            primary_edges = []
            secondary_edges = []
            secondary_node_distance = []

            # Get Immediate Edges. Add them to a queue to then search their potential edges
            check_queue = []
            for conn_node in self.graph_dict[node]:
                primary_edges.append((node, conn_node))
                if conn_node != node:
                    check_queue.append(conn_node)

            if verbose:
                print("*Check Start", check_queue)

            # Loop During Check Queue
            until_path_increment = len(check_queue)
            path_distance_to_node = 1
            previous_nodes = [node]
            while True:
                # Check
                if len(check_queue) == 0:
                    break
                check_node = check_queue[0]
                if verbose:
                    print("*ON:", check_node)
                    print("*PREVIOUS:", previous_nodes)

                # Doc Doc Doc
                for check_conn_node in self.graph_dict[check_node]:
                    if len(self.graph_dict[check_node]) == 1:
                        if verbose:
                            print("LEAF", check_node)
                        new_edge = (check_node, check_conn_node)
                        secondary_edges.append(new_edge)
                        secondary_node_distance.append((check_node, path_distance_to_node))
                        continue
                    if check_conn_node in previous_nodes:
                        if verbose:
                            print("NOPE - Previous", check_conn_node, self.graph_dict[check_node], check_queue)
                        continue
                    if check_conn_node == check_node:
                        if verbose:
                            print("NOPE - Check Node", check_conn_node, self.graph_dict[check_node], check_queue)
                        continue

                    check_queue.append(check_conn_node)
                    if verbose:
                        print("YES", check_conn_node, self.graph_dict[check_node], check_queue)

                    new_edge = (check_node, check_conn_node)
                    if new_edge not in secondary_edges:
                        if verbose:
                            print("NEW", new_edge)
                            print("DIS", check_node, path_distance_to_node)
                        secondary_edges.append(new_edge)
                        secondary_node_distance.append((check_node, path_distance_to_node))

                previous_nodes.append(check_node)
                until_path_increment -= 1
                previous_nodes.append(check_node)
                del check_queue[0]

                if until_path_increment == 0:
                    until_path_increment = len(check_queue)
                    path_distance_to_node += 1

            branch_dict[node]["primary_edges"] = set(primary_edges)
            branch_dict[node]["secondary_edges"] = set(secondary_edges)
            branch_dict[node]["secondary_edges_with_distance"] = set(secondary_node_distance)

        self.branch_dict = branch_dict

    def _calc_main_branch(self):
        """
        Main branch is the longest un-interrupted path in the graph. Could be multiple.
        """

        max_distance = 0
        for node in self.branch_dict:
            try:
                node_max = max([d[1] for d in self.branch_dict[node]["secondary_edges_with_distance"]])
            except ValueError:  # Isolated Node Edge Case
                node_max = 0
            max_distance = node_max if node_max > max_distance else max_distance

        main_edge = []
        for node in self.branch_dict:
            for edge in self.branch_dict[node]["secondary_edges_with_distance"]:
                if edge[1] == max_distance:
                    main_edge.append(edge)

        # Try to determine Root Node - It's name will appear most often in main_branch if applicable.
        node_names = [v[0] for v in main_edge]
        name_count = {v: 0 for v in node_names}
        for n in node_names:
            name_count[n] += 1
        max_count = max([name_count[k] for k in name_count])
        root_node = [n for n in name_count if name_count[n] == max_count]

        # From the two furthest edges in main branch, reconstruct the path between to include all nodes.
        # Starting with root node(or one of them)
        # TODO

        self.info["root_node"] = root_node
        self.info["max_distance"] = max_distance
        self.info["main_edge"] = main_edge

    def _calc_leaf_branch(self):
        """
        Leaf branches/nodes are terminal nodes.
        """

        terminal_nodes = set()

        # Terminal Nodes are only connected to a single other
        for n in self.branch_dict:
            if len(self.branch_dict[n]["primary_edges"]) == 1:
                terminal_nodes.add(n)

        # We've already calculated the longest/main branch. So exclude those from the terminal ones.
        main_edge_nodes = {v[0] for v in self.info["main_edge"]}
        leaf_nodes = terminal_nodes.difference(main_edge_nodes)

        # print(terminal_nodes)
        # print(main_edge_nodes)
        # print(leaf_nodes)
        #print(self.branch_dict)

if __name__ == "__main__":

    g = {"a": ["d"],
         "b": ["c", "f"],
         "c": ["b", "d", "e"],
         "d": ["a", "c"],
         "e": ["c"],
         "f": ["b"],
         }

    graph = Graph(g)

    print(graph.graph_dict)

    # print("Vertices of graph:")
    # print(graph.get_nodes())
    #
    # print("Edges of graph:")
    # print(graph.get_edges())

    # print(graph.branch_dict)


    # print("AHH")
    # a = graph.find_longest_branch()
    # print(a)

    # print(graph.info)