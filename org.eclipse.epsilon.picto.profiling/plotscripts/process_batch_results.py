#!/usr/bin/env python
# Usage: ./process_batch_results.py <path_to_results.csv>

import pandas as pd
import sys

n_element = "Model"
n_time = "BatchTimeMillis"
n_avg_time = "AvgTimeMillis"
n_std_time = "StdTimeMillis"

processed_pattern = "{}_processed.csv"


def process_batch_results(filename):
    df = pd.read_csv(filename)

    # drop max values for each model
    # TODO: decide if this is necessary / if we need something different
    # df_models = []
    # for model in df[n_element].unique():
    #     df_model = df[df[n_element] == model].copy()
    #     df_model = df_model.loc[~df_model[n_time].isin([df_model[n_time].max()])]
    #     df_models.append(df_model)

    # # Recombine individual dataframes
    # df = df_models.pop()
    # while len(df_models) > 0:
    #     df = df.append(df_models.pop())

    # Group by
    df = df.groupby([n_element])[n_time].agg(["mean", "std"]).reset_index()
    df.columns = [n_element, n_avg_time, n_std_time]
    return df


if __name__ == "__main__":
    # filename = "../batchResults.csv"
    filename = sys.argv[1]
    df = process_batch_results(filename)
    df.to_csv(processed_pattern.format(filename), index=False)
