#!/usr/bin/env python
# Usage: ./batch_results.py <path_to_results.csv>
# ./batch_results.py batchResults.csv

import pandas as pd
import sys

n_element = "Model"
n_time = "BatchTimeMillis"

filename = sys.argv[1] if len(sys.argv > 1) else "../batchResults.csv"
df = pd.read_csv(filename)
df.head()

# drop max values for each model
df_models = []
for model in df[n_element].unique():
    df_model = df[df[n_element] == model].copy()
    df_model = df_model.loc[~df_model[n_time].isin([df_model[n_time].max()])]
    df_models.append(df_model)

# Recombine individual dataframes
df = df_models.pop()
while len(df_models) > 0:
    df = df.append(df_models.pop())

# Group by
df = df.groupby([n_element])[n_time].mean().reset_index()
df.to_csv("{}_processed.csv".format(filename), index=False)
