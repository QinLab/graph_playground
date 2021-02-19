import sys
from models.yolo_csv import YoloCSV
from models.yolo_tree import YoloTree
from models.yolo_plot import YoloPlot
from models.i_graph import graph_to_i_graph

from models.yolo_csv_copy import YoloCSV as YoloCSVold

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

    trap_num = 1
    t_stop = 20

    if len(sys.argv) == 3:
        trap_num = int(sys.argv[1])
        t_stop = int(sys.argv[2])

    yolo = YoloCSV("data/FT_BC8_yolo_short.csv")
    graph_dict, yolo_trap_time = yolo.to_graph_dict(trap_num=trap_num, t_stop=t_stop)
    print(graph_dict)
    print("Tree Start")
    tree = YoloTree(graph_dict)
    print("Tree Dict")
    print(tree.tree_dict)
    print(tree.tree_info)

    plot = YoloPlot(tree, yolo_trap_time)
    plot.show()

    # print(graph.info)

    # graph_to_i_graph(graph_dict)


if __name__ == "__main__":

    main()
