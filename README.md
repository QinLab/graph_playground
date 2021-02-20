# graph_playground
<p>
Exploratory repo for graph/tree analysis and visualization
</p>

# Installation
<p>
Python 3.8.1
Requirements.txt, as usual, venv recommended.
</p>

# Use
<p>
Will try to keep this updated as codebase develops, but in context
of the yolo_cell.csv, can do the following:

1. navigate into /src
2. python run_yolo.csv {trap_num} {t_stop}

I purposely don't have the raw data csv committed, but it is expected to be
in src/data. Path reference in run_yolo.csv.

Will generate some output and launch plotly into a local webpage.

Example:

```
python run_yolo.csv 1 30
```
Will query the raw data.csv on trap_num 1 from time_num 0 to 30 (inclusive).  To help with debug, the subset of the raw data that the query pulled will create in src/data under recent_query.csv, easier to look through that than the source file.
</p>

# Organization
<p>
In context of the yolo.csv data, currently based on the interaction
of 3 classes/.py files in src/models:

1. yolo_csv.py, parses the raw data into an undirected graph and returns some
   context specific metadata specific to the subset of the raw data used to generate
   it.
2. yolo_tree.py, refines the output of yolo_csv into a more friendly tree-like 
   structure in the context of the project.
3. yolo_plot.py, concerned with visualization of the output of yolo_tree.

Additionally there may be some other random stuff in src/models or workbooks that
I'm currently (or previously was) playing around with. Can ignore that stuff.
</p>



