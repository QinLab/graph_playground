import pandas as pd

"""
Doc Doc Doc


Notes:

Split occurs when multiple objs exist in same trap and share the same predeccorID?
"""

# def print_yolo_row(r):



class YoloCellCSV:

    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self._on_init()

    def _on_init(self):
        self.df = pd.read_csv(self.file_path)
        self.df = self.df.fillna(1).astype(int)     # Done mainly set that first NA predecessorID to 1 (I think that's ok?)

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
            print(trap, pred_ids)

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

        print(query)
        return self.df.query(query)


def main():

    cats = YoloCellCSV("FT_BC8_yolo_short.csv")
    # cats.describe_all()
    # cats.describe_trap(1, t_start=0, t_stop=12, pred_id=1)

    a = cats.query(trap_num=1, t_start=0, t_stop=30)
    print(a.columns.tolist())
    for i, v in a.iterrows():
        print(v.astype(str).values.flatten().tolist())




if __name__ == "__main__":

    main()
