import igraph
from igraph import Graph as IGraph
from igraph import EdgeSeq
import plotly.graph_objects as go

"""
Doc Doc Doc

https://igraph.org/python/doc/tutorial/tutorial.html
"""

def graph_to_i_graph(graph_dict):

    # print(graph_dict)

    i_graph = IGraph()
    i_graph.add_vertices(len(graph_dict))

    # Assign Integers to the Vertices/Nodes
    # Dicts are ordered in Python 3.6+ :)
    node_index_lu = {n:i for i, n in enumerate(graph_dict)}
    index_node_lu = {i:n for i, n in enumerate(graph_dict)}

    # Now lets add some edges
    for n in graph_dict:
        edges = graph_dict[n]
        parent_i = node_index_lu[n]
        children_i = [node_index_lu[n] for n in edges]
        i_graph.add_edges([(parent_i, c_i) for c_i in children_i])

    # print(node_index_lu)

    print(i_graph)

    # Taken from web, still need to work through some.
    num_nodes = len(graph_dict)
    node_label = list(map(str, range(num_nodes)))
    layout = i_graph.layout('rt')  # Not sure what 'rt' is atm.

    position = {k: layout[k] for k in range(num_nodes)}
    Y = [layout[k][1] for k in range(num_nodes)]
    M = max(Y)

    # es = EdgeSeq(i_graph)  # sequence of edges
    E = [e.tuple for e in i_graph.es]  # list of edges

    L = len(position)
    Xn = [position[k][0] for k in range(L)]
    Yn = [2 * M - position[k][1] for k in range(L)]
    Xe = []
    Ye = []
    for edge in E:
        Xe += [position[edge[0]][0], position[edge[1]][0], None]
        Ye += [2 * M - position[edge[0]][1], 2 * M - position[edge[1]][1], None]

    labels = [index_node_lu[int(v)] for v in node_label]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Xe,
                             y=Ye,
                             mode='lines',
                             line=dict(color='rgb(210,210,210)', width=1),
                             hoverinfo='none'
                             ))
    fig.add_trace(go.Scatter(x=Xn,
                             y=Yn,
                             mode='markers',
                             name='bla',
                             marker=dict(symbol='circle-dot',
                                         size=18,
                                         color='#6175c1',  # '#DB4551',
                                         line=dict(color='rgb(50,50,50)', width=1)
                                         ),
                             text=labels,
                             hoverinfo='text',
                             opacity=0.8
                             ))

    fig.show()