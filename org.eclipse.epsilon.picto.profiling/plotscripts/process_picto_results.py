#!/usr/bin/env python
# Usage: ./process_picto_results.py <profiling_csv_file>

import numpy as np
import pandas as pd
import sys


n_element = "Element"
n_time = "TimeMillis"
n_count = "Count"

views_avg = "views_avg"
n_std_time = "views_std"
n_std_ratio = "views_std_ratio"

n_tree_viewer_avg = "treeviewer_avg"
n_singleview_avg = "single_view_avg"


n_treeViewer_row = "TreeViewer"

n_numviews = "num_views"

processed_pattern = "{}_processed.csv"


def process_picto_results (filename):
    df = pd.read_csv(filename)

    accum = 0
    views_computation = []
    treeviewer_computation = []
    num_views = 0
    for _, row in df.iterrows():
        if row[n_element] == n_treeViewer_row:
            treeviewer_computation.append(row[n_time])
            if accum != 0:
                views_computation.append(accum)
                accum = 0
                num_views = 0
        else:
            num_views += 1
        accum += row[n_time]

    views_computation.append(accum) # last one


    tree_viewer_avg = np.average(treeviewer_computation)
    views_avg = np.average(views_computation)
    views_std = np.std(views_computation)
    views_stdratio = views_std / views_avg
    single_view_avg = views_avg / num_views

    result = [{ "treeviewer_avg" : tree_viewer_avg,
                "views_avg" : views_avg,
                "views_std" : views_std,
                "views_std_ratio" : views_stdratio,
                "num_views" : num_views,
                "single_view_avg" : single_view_avg}]
    result_df = pd.DataFrame.from_records(result)

    return result_df


if __name__ == "__main__":
    # The profiling file
    # filename = sys.argv[1]

    # or

    filename = "/home/fonso/Sync/papers/2023-pictoJournal/2023-picto-vm10700/RevEngSirius.ecore.profiling.csv"

    df = process_picto_results(filename)
    df.to_csv(processed_pattern.format(filename), index=False)
