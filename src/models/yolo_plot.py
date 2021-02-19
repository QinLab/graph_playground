import plotly.graph_objects as go
import sys

"""

XN [-1.0, -1.0, -1.0, -1.0, 0.0, 0.0, 1.0, 0.0, 1.0]
Yn [4.0, 5.0, 6.0, 7.0, 8.0, 7.0, 7.0, 6.0, 6.0]
traces ['1.1', '2.1', '3.1', '4.1', '5.1', '6.1', '6.2', '7.1', '7.2']

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
"""


class YoloPlot:

    def __init__(self, yolo_tree, yolo_trap_time):
        self.yolo_tree = yolo_tree
        self.yolo_trap_time = yolo_trap_time
        self.fig = go.Figure()
        self.plot_info = {}
        self._on_init()


    def _on_init(self):
        """
        Doc Doc Doc
        """

        self._plot_info_from_tree_dict()
        self.fig.update_xaxes(range=[0.0, float(self.plot_info["x_bound"])])
        self.fig.update_yaxes(range=[0.0, float(self.plot_info["y_bound"])])
        self.fig.layout.title["text"] = "TrapNum:{} TStop:{}".format(self.yolo_trap_time["trap_num"],
                                                                     self.yolo_trap_time["t_stop"])

        # Root Node(s)
        self.plot_info["root_pos"] = {}
        root_trace = self._get_root_traces()
        self.add_trace(root_trace)

        # Main Branch(s)
        main_trace = self._get_main_branch_traces()
        self.add_trace(main_trace)

        # Daughter Branch(s)
        daughter_trace = self._get_daughter_branch_traces()
        self.add_trace(daughter_trace)

    def _plot_info_from_tree_dict(self):
        """
        Doc Doc Doc
        """

        # To Establish X Bounds, check for max length of main branches
        max_main_branch_length = 0
        for n in self.yolo_tree.tree_info["root_nodes"]:
            main_branch_length = len(self.yolo_tree.tree_dict[n])
            if main_branch_length > max_main_branch_length:
                max_main_branch_length = main_branch_length

        # To Establish Y bounds, check for max length of daughter branches
        daughter_nodes = [n for n in self.yolo_tree.tree_dict if n not in self.yolo_tree.tree_info["root_nodes"]]
        max_daughter_branch_length = 0
        for n in daughter_nodes:
            daughter_branch_length = len(self.yolo_tree.tree_dict[n])
            if daughter_branch_length > max_daughter_branch_length:
                max_daughter_branch_length = daughter_branch_length

        self.plot_info["x_bound"] = max_main_branch_length + 2
        self.plot_info["y_bound"] = (max_daughter_branch_length + 2)*2


    def _get_root_traces(self):
        """
        Doc Doc Doc
        """

        x_arr = []
        y_arr = []
        labels = []

        num_root = len(self.yolo_tree.tree_info["root_nodes"])
        y_offset = self.plot_info["y_bound"] / (num_root+1)
        for i, n in enumerate(self.yolo_tree.tree_info["root_nodes"]):
            x = float(n.split(".", 1)[0])
            y = (i+1)*y_offset   # Fix this when multiple root nodes...
            x_arr.append(x)
            y_arr.append(y)
            labels.append(n)
            self.plot_info["root_pos"][n] = {"x": x, "y": y}

        return {"x": x_arr, "y": y_arr, "labels": labels, "color": "#008000", "name": "mC-R"}

    def _get_main_branch_traces(self):
        """
        Doc Doc Doc
        """

        x_arr = []
        y_arr = []
        labels = []

        for r_n in self.yolo_tree.tree_info["root_nodes"]:

            for n in self.yolo_tree.tree_dict[r_n]:
                x = float(n.split(".", 1)[0])
                y = self.plot_info["root_pos"][r_n]["y"]
                x_arr.append(x)
                y_arr.append(y)
                labels.append(n)

        return {"x": x_arr, "y": y_arr, "labels": labels, "color": "#008000", "name": "mC"}


    def _get_daughter_branch_traces(self):
        """
        Doc Doc Doc
        """

        x_arr = []
        y_arr = []
        labels = []

        y_offset = 1  # Visually nicer, alternates branches...

        for d_n in self.yolo_tree.tree_dict:
            if d_n in self.yolo_tree.tree_info["root_nodes"]:
                continue

            # Find node in main branch where daughter node connects
            main_daughter_edge = list(filter(lambda x: x[1] == d_n, self.yolo_tree.tree_info["branch_edges"]))[0]

            # Get Y-val of that main branch by finding the root node of the parent edge node
            main_root_node_y = None
            for r_n in self.yolo_tree.tree_dict:
                if main_daughter_edge[0] in self.yolo_tree.tree_dict[r_n]:
                    try:
                        main_root_node_y = self.plot_info["root_pos"][r_n]["y"]
                    except KeyError as e:
                        print("BROKE YOLOPLOT 147")
                        print(e)
                        print(d_n)
                        print(main_daughter_edge)
                        sys.exit()
                    break

            # Add root of daughter branch
            x = float(main_daughter_edge[0].split(".", 1)[0])
            y = main_root_node_y + (1 * y_offset)
            x_arr.append(x)
            y_arr.append(y)
            labels.append(d_n)

            # Add nodes in daughter branch
            for i, n in enumerate(self.yolo_tree.tree_dict[d_n]):
                i += 2
                x = float(main_daughter_edge[0].split(".", 1)[0])
                y = main_root_node_y + (i*y_offset)
                x_arr.append(x)
                y_arr.append(y)
                labels.append(n)

            y_offset *= -1

        return {"x": x_arr, "y": y_arr, "labels": labels, "color": "#FFA500", "name": "dC"}


    def add_trace(self, trace_info):
        """
        Doc Doc Doc
        """

        self.fig.add_trace(go.Scatter(x=trace_info["x"],
                                      y=trace_info["y"],
                                      mode='markers',
                                      name=trace_info["name"],
                                      marker=dict(symbol='circle-dot',
                                                  # size=36,
                                                  color=trace_info["color"],
                                                  line=dict(color='rgb(0,0,0)', width=0.5)
                                                  ),
                                      text=trace_info["labels"],
                                      textfont=dict(color='#000000'),
                                      hoverinfo='text',
                                      opacity=0.8
                                      ))





    def show(self):

        self.fig.show()
