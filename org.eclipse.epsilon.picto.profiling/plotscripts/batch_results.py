#!/usr/bin/env python
# Usage: ./batch_results.py <path_to_results.csv>
# ./batch_results.py batchResults.csv

import pandas as pd
import sys

n_element = "Model"
n_time = "BatchTimeMillis"
n_avg_time = "AvgTimeMillis"
n_std_time = "StdTimeMillis"

# filename = "../batchResults.csv"
filename = sys.argv[1]

df = pd.read_csv(filename)
df.head()

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
df.to_csv("{}_processed.csv".format(filename), index=False)
