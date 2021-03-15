import sys
import os
from models.yolo_csv import YoloCSV
from models.yolo_tree import YoloTree
from models.yolo_plot import YoloPlot

"""
Doc Doc Doc
"""


def main():

    if not os.path.exists("data"):
        os.mkdir("data")
        print("/data did not exist, creating. Need to add raw_data.csv here and update path below if applicable")
        sys.exit()

    trap_num = 1
    t_stop = 20

    if len(sys.argv) == 3:
        trap_num = int(sys.argv[1])
        t_stop = int(sys.argv[2])

    yolo = YoloCSV("data/FT_BC8_yolo_short.csv")
    graph_info = yolo.to_graph_info(trap_num=trap_num, t_stop=t_stop)
    print("Graph Dict")
    print(graph_info)
    print(graph_info["check_data"])
    tree = YoloTree(graph_info)
    print("Tree Dict")
    print(tree.tree_dict)
    print("Tree Info")
    print(tree.tree_info)

    plot = YoloPlot(tree, graph_info)
    plot.show()


if __name__ == "__main__":

    main()
