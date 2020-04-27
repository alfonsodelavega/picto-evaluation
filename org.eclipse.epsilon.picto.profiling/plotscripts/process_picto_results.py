#!/usr/bin/env python
# Usage: ./picto_plot.py <profiling_csv_file> <time_for_batch_processing>
# Example: ./picto_plot.py comps.ecore.profiling.csv 600

import pandas as pd
import sys

n_element = "Element"
n_time = "TimeMillis"
n_avg_time = "AvgTimeMillis"
n_std_time = "StdTimeMillis"
n_views_avg = "AvgAcrossviews"
n_cum_time = "Accumulated Time (ms)"
n_treeViewer_row = "TreeViewer"
n_pos = "# Rendered Views"

processed_pattern = "{}_processed.csv"


def process_picto_results (filename):
    df = pd.read_csv(filename)

    #TODO: Decide if it is necessary to remove best/worst obtained time

    df = df.groupby([n_element])[n_time].agg(["mean", "std"]).reset_index()
    df.columns = [n_element, n_avg_time, n_std_time]

    # x axis position
    # The tree viewer time should be the axis 0 value
    # (not sure about the order of the others, alphanumeric atm)
    #TODO: decide order of rendered views
    df[n_pos] = df.index + 1
    df.set_index(n_element, inplace=True)
    df.at[n_treeViewer_row, n_pos] = 0
    df.sort_values(by=[n_pos], inplace=True)

    # Average view rendering times to get a uniform graph
    df[n_views_avg] = df[n_avg_time].mean()

    # Get accumulated times as new views are rendered
    df[n_cum_time] = df[n_views_avg].cumsum()
    return df

if __name__ == "__main__":
    # The profiling file
    filename = sys.argv[1]
    # The time it took the batch M2T transformation to complete (used in plot below)
    # batch_time = float(sys.argv[2])

    # or

    # filename = "../models/comps.ecore.profiling.csv"
    # batch_time = 250

    df = process_picto_results(filename)
    df.to_csv(processed_pattern.format(filename), index=False)
