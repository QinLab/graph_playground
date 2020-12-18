import csv

"""
Test
Doc Doc Doc
"""

def load_csv(file_path):

    with open(file_path, "r", encoding="utf-8") as r_file:
        reader = csv.reader(r_file, delimiter=",")
        return [row for row in reader]
