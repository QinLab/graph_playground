import pandas as pd
import math
from .graph import Graph

"""
Doc Doc Doc


Notes:

Split occurs when multiple objs exist in same trap and share the same predeccorID?
"""

class YoloCSV:

    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self._on_init()

    def _on_init(self):
        self.df = pd.read_csv(self.file_path)
        # self.df = self.df.fillna(1).astype(int)     # Done mainly set that first NA predecessorID to 1 (I think that's ok?)
        ## ^^ Will revist.

    def describe_all(self):
        """
        Just getting familiar w/ the data/taking a look at various relationships.

        Some notes
        trap_num:
        time_num:
        total_objs: total number of cells in the image
        predecessorID: label ID for each cell in each image for tracking
        """

        print("Head")
        print(self.df.head())
        print("Unique K/V")
        for k in self.df.columns:
            u_v = self.df[k].unique()
            print(k, len(u_v), u_v)

        for trap in self.df["trap_num"].unique():
            pred_ids = self.df.query("trap_num == {}".format(trap))["predecessorID"].unique()
         #   print(trap, pred_ids)

    def describe_trap(self, trap_num, t_start=None, t_stop=None, pred_id=None):
        """
        Queries a specific trap. Optional args from narrowing down time period and pred_id

        -- Mostly replaced w/ self.query(), prob change this to something else
        """

        t_start = self.df["time_num"].min() if not t_start else t_start
        t_stop = self.df["time_num"].max() if not t_stop else t_stop

        query = "trap_num == {} and {} <= time_num <= {}".format(trap_num, t_start, t_stop)
        if pred_id:
            query += " and predecessorID == {}".format(pred_id)
        df = self.df.query(query)
        for i, v in df.iterrows():
            print(v)

        print(len(df.index))

    def query(self, trap_num=None, t_start=None, t_stop=None, total_objs=None, pred_id=None):

        query = ""

        if trap_num:
            query += "trap_num == {}".format(trap_num)

        if t_start and t_stop:
            query += " and {} <= time_num <= {}".format(t_start, t_stop)
        else:
            if t_start:
                query += " and time_num >= {}".format(t_start)
            if t_stop:
                query += " and time_num <= {}".format(t_stop)

        if total_objs:
            query += " and total_objs == {}".format(total_objs)

        if pred_id:
            query += " and predecessorID == {}".format(pred_id)

        # Clean Up
        if query[0] == " ":
            query = query[5:]

        # print(query)
        return self.df.query(query)

    def df_to_graph_dict(self):
        """
                g = {"a": ["d"],
                 "b": ["c", "f"],
                 "c": ["b", "c", "d", "e"],
                 "d": ["a", "c"],
                 "e": ["c"],
                 "f": [],
            #    "g": ["f"],
             #   "z": ["f"]
                 }
        """

        graph_dict = {}

        df = self.query(trap_num=1, t_start=0, t_stop=30)

        last_node_name = None
        last_pred_id = None

        last_branch_node_name = None
        last_branch_pred_id = None

        for t in df["time_num"].unique():

            time_df = df.query("time_num == {}".format(t))
            # print(t, len(time_df.index))

            len_time_step = len(time_df.index)

            # In Length Just One, No Branching
            if len_time_step == 1:
             #   print("Single Time Step")
                vals = time_df.to_dict('records')[0]
                pred_id = vals["predecessorID"]
                if math.isnan(pred_id):
                    #    print("NaN: ", pred_id)
                    pred_id = 1

                node_name = "{}.{}".format(vals["time_num"], int(pred_id))
                graph_dict[node_name] = []
                if last_node_name:
                    graph_dict[node_name].append(last_node_name)
                    graph_dict[last_node_name].append(node_name)

                last_node_name = node_name
                last_pred_id = pred_id
                continue

            # Branching
            step_info = time_df.to_dict('records')
            step_info = [[step_info[k] for k in step_info] for step_info in step_info]
            step_info = [list(x) for x in set(tuple(x) for x in step_info)]
            # Branch at this node.
            if len(step_info) == 1:
            #    print("New Branch Time Step")
                vals = time_df.to_dict('records')[0]
                pred_id = vals["predecessorID"]
                # if math.isnan(pred_id):
                #    print("NaN: ", pred_id)
                # pred_id = 1

                node_name = "{}.{}".format(vals["time_num"], int(pred_id))
                graph_dict[node_name] = []
                if last_node_name:
                    graph_dict[node_name].append(last_node_name)
                    graph_dict[last_node_name].append(node_name)

                last_node_name = node_name
                last_pred_id = pred_id
                last_branch_node_name = node_name
                last_branch_pred_id = pred_id
                continue

            #print("Co-existing Time Stamp")
            for i, v in time_df.iterrows():
               #  print(v.astype(str).values.flatten().tolist())
                time_num = v["time_num"]
                pred_id = v["predecessorID"]
                # Edge Case
                if math.isnan(pred_id):
                #    print("NaN: ", v)
                    pred_id = 1.0

                node_name = "{}.{}".format(int(time_num), int(pred_id))

                if pred_id == last_branch_pred_id:
                    if node_name not in graph_dict:
                        graph_dict[node_name] = []
                        graph_dict[node_name].append(last_node_name)
                        graph_dict[last_node_name].append(node_name)
                        last_node_name = node_name
                        last_pred_id = pred_id
                else:
                    if node_name not in graph_dict:
                        graph_dict[node_name] = []
                        graph_dict[node_name].append(last_branch_node_name)
                        graph_dict[last_branch_node_name].append(node_name)
                        last_branch_node_name = node_name
                        last_branch_node_name = node_name
                        last_brand_pred_id = pred_id



        return graph_dict

        #
        #
        # print("*")
        # print(tree_dict)
        #
        # print("*")
        # for i, v in df.iterrows():
        #     print(v.astype(str).values.flatten().tolist())

            # a = Graph(tree_dict)
            # branch = a.find_longest_branch()
            #
            # print("*")
            # print(branch)


def main():

    pass
    # cats = YoloCellCSV("FT_BC8_yolo_short.csv")
    # # cats.describe_all()
    # # cats.describe_trap(1, t_start=0, t_stop=12, pred_id=1)
    #
    # # a = cats.query(trap_num=1, t_start=0, t_stop=10)
    # # print(a.columns.tolist())
    # # for i, v in a.iterrows():
    # #     print(v.astype(str).values.flatten().tolist())
    #
    # # YoloCellCSV.df_to_tree_dict(a)
    #
    # cats.df_to_tree_dict_two()


if __name__ == "__main__":

    main()