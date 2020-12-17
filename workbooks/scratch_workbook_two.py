


"""
Building/Traversing Graphs/Trees from scratch.

This is me messing around without much background reading on the subject to get a rough idea of whats going on.

Graph class copied from web and I've been using it to build off of.
"""


class Graph(object):
    def __init__(self, graph_dict={}):
        """ initializes a graph object
            If no dictionary or None is given,
            an empty dictionary will be used
        """
        self.graph_dict = graph_dict

    def get_vertices(self):
        """ returns the vertices of a graph """
        return list(self.graph_dict)

    def get_edges(self):
        """ returns the edges of a graph """
        return self.generate_edges()

    def add_vertex(self, vertex):
        """ If the vertex "vertex" is not in
            self.__graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary.
            Otherwise nothing has to be done.
        """
        if vertex not in self.graph_dict:
            self.graph_dict[vertex] = []

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list;
            between two vertices can be multiple edges!
        """
        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self.graph_dict:
            self.graph_dict[vertex1].append(vertex2)
        else:
            self.graph_dict[vertex1] = [vertex2]

    def generate_edges(self):
        """ A static method generating the edges of the
            graph "graph". Edges are represented as sets
            with one (a loop back to the vertex) or two
            vertices
        """
        edges = []
        for vertex in self.graph_dict:
            for neighbour in self.graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def find_longest_branch(self):
        """
        Took a couple hours to work through this but looks to be working. Need to clean it up some.

        I found a "correct" implementation and it appears to be similar, so look to be on the right track.
        https://www.geeksforgeeks.org/longest-path-undirected-tree/
        """
        branch_dict = {}

        # Iterate though all the nodes
        for node in self.graph_dict:
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

            print("*Check Start", check_queue)

            # Loop During Check Queue
            until_path_increment = len(check_queue)
            path_distance_to_node = 1
            previous_nodes = [node]
            while True:
                # print("Initial")
                # print(len(check_queue))
                # print(until_path_increment)
                # print(check_queue)
                # Check
                if len(check_queue) == 0:
                    break
                check_node = check_queue[0]
                print("*ON:", check_node)
                print("*PREVIOUS:", previous_nodes)

                # Doc Doc Doc
                for check_conn_node in self.graph_dict[check_node]:
                    if len(self.graph_dict[check_node]) == 1:
                        print("LEAF", check_node)
                        new_edge = (check_node, check_conn_node)
                        secondary_edges.append(new_edge)
                        secondary_node_distance.append((check_node, path_distance_to_node))
                        continue
                    if check_conn_node in previous_nodes:
                        print("NOPE", check_conn_node, self.graph_dict[check_node], check_queue)
                        continue
                    if check_conn_node == check_node:
                        print("NOPE2", check_conn_node, self.graph_dict[check_node], check_queue)
                        continue

                    check_queue.append(check_conn_node)
                    print("YES", check_conn_node, self.graph_dict[check_node], check_queue)

                    new_edge = (check_node, check_conn_node)
                    if new_edge not in secondary_edges:
                        print("NEW", new_edge)
                        print("DIS", check_node, path_distance_to_node)
                        secondary_edges.append(new_edge)
                        secondary_node_distance.append((check_node, path_distance_to_node))
                previous_nodes.append(check_node)
                # input()

                until_path_increment -= 1
                previous_nodes.append(check_node)
                del check_queue[0]

                if until_path_increment == 0:
                    until_path_increment = len(check_queue)
                    path_distance_to_node += 1

            branch_dict[node]["primary_edges"] = set(primary_edges)
            branch_dict[node]["secondary_edges"] = set(secondary_edges)
            branch_dict[node]["secondary_edges_with_distance"] = set(secondary_node_distance)

        # Calc Max Distances
        max_distance = 0
        max_branches = [(k, k, max_distance) for k in branch_dict]
        for node in branch_dict:
            if not branch_dict[node]["primary_edges"]:
                continue
            max_node_dis = max(v[1] for v in branch_dict[node]["secondary_edges_with_distance"])
            max_nodes = list(filter(lambda x: x[1] == max_node_dis, branch_dict[node]["secondary_edges_with_distance"]))
            print(max_node_dis)
            if max_node_dis > max_distance:
                max_distance = max_node_dis
                max_branches = [[node]+list(v) for v in max_nodes]
                continue
            if max_node_dis == max_distance:
                max_branches += [[node]+list(v) for v in max_nodes]

        # print("Distance")
        # print(max_distance)
        # print(max_branches)

        branch_dict["max_distance"] = max_distance
        branch_dict["max_branches"] = max_branches

        return branch_dict


    def __str__(self):
        res = "vertices: "
        for k in self.graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.generate_edges():
            res += str(edge) + " "
        return res


if __name__ == "__main__":
    g = {"a": ["d"],
         "b": ["c", "f"],
         "c": ["b", "c", "d", "e"],
         "d": ["a", "c"],
         "e": ["c"],
         "f": ["b", "g", "z"],
         "g": ["f"],
         "z": ["f"]
         }

    graph = Graph(g)

    print("Vertices of graph:")
    print(graph.get_vertices())

    print("Edges of graph:")
    print(graph.get_edges())

    # print("Add vertex:")
    # graph.add_vertex("z")

    print("Vertices of graph:")
    print(graph.get_vertices())

    # print("Add an edge:")
    # graph.add_edge({"a", "z"})
    #
    # print("Vertices of graph:")
    # print(graph.get_vertices())
    #
    # print("Edges of graph:")
    # print(graph.get_edges())
    #
    # print('Adding an edge {"x","y"} with new vertices:')
    # graph.add_edge({"x", "y"})
    # print("Vertices of graph:")
    # print(graph.get_vertices())
    # print("Edges of graph:")
    # print(graph.get_edges())

    print("AHH")
    a = graph.find_longest_branch()
    print(a)

