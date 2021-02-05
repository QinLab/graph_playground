from models.yolo_csv import YoloCSV
from models.graph import Graph
from models.i_graph import graph_to_i_graph

"""
Doc Doc Doc

Test Graph
g = {"a": ["d"],
     "b": ["c", "f"],
     "c": ["b", "c", "d", "e"],
     "d": ["a", "c"],
     "e": ["c"],
     "f": [],
    }
"""


def main():

    yolo = YoloCSV("data/FT_BC8_yolo_short.csv")
    graph_dict = yolo.df_to_graph_dict()
    print("Not Dynamic - But Hard-code to Trap 1 Tmax of 30")
    print("Graph Crashes/Hangs up at Tmax of 50... So need to look into that")
    print(graph_dict)

    # graph_dict = {"a": ["d"],
    #               "b": ["c", "f"],
    #               "c": ["b", "c", "d", "e"],
    #               "d": ["a", "c"],
    #               "e": ["c"],
    #               "f": [],
    #               }

    graph = Graph(graph_dict)

    print(graph.info)

    graph_to_i_graph(graph_dict)


if __name__ == "__main__":

    main()
