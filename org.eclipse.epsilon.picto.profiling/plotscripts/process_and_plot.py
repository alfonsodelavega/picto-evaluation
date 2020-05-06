#!/usr/bin/env python
# Usage:
# ./process_and_plot.py <results.csv> <parallel_results.csv > <models_folder>

# This script both processes the raw csv files from the batch and picto
# executions, and generates a single plot that contains all model graphs

import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
from process_batch_results import process_batch_results, processed_pattern, n_element
from process_picto_results import process_picto_results, n_pos, n_avg_time, n_cum_time

profiling_pattern = "{}.profiling.csv"
full_plot_pattern = "{}_fullplot.pdf"

save_intermediate_results = True  # True: saves processed csvs

if __name__ == "__main__":
    # The batch single-core raw results file
    batch_file = sys.argv[1]
    # The batch parallel raw results file
    batch_parallel_file = sys.argv[2]
    # The models folder
    models_folder = sys.argv[3]

    df_batch = process_batch_results(batch_file)
    df_batch_parallel = process_batch_results(batch_parallel_file)
    if save_intermediate_results:
        df_batch.to_csv(processed_pattern.format(batch_file),
                        index=False)
        df_batch_parallel.to_csv(processed_pattern.format(batch_parallel_file),
                                 index=False)

    models = df_batch[n_element].unique()

    plt.rcParams["figure.figsize"] = (10 , 7 * len(models))
    f, axes = plt.subplots(nrows=len(models), ncols=1)

    for model, ax in zip(models, axes):
        batch_time = df_batch[ df_batch[n_element] == model ][n_avg_time].iloc[0]
        batch_parallel_time = df_batch_parallel[
            df_batch_parallel[n_element] == model ][n_avg_time].iloc[0]

        model_path = models_folder + profiling_pattern.format(model)
        model_df = process_picto_results(model_path)
        if save_intermediate_results:
            model_df.to_csv(processed_pattern.format(model_path), index=True)

        ax.plot((0, model_df[n_pos].iat[-1]), (batch_time, batch_time),
                color="red", label="singleCPU")
        ax.plot((0, model_df[n_pos].iat[-1]), (batch_parallel_time, batch_parallel_time),
                color="green", label="multiCPU")
        ax.plot(model_df[n_pos], model_df[n_cum_time],
                linestyle='-',
                # marker='o',
                color='b', label="picto")
        ax.set_ylim(bottom=0)
        ax.set_xlim([0, model_df[n_pos].iat[-1]])
        ax.set_xlabel(n_pos)
        ax.set_ylabel(n_cum_time)
        ax.set_title(model)
        ax.legend()

    f.savefig(full_plot_pattern.format(batch_file), bbox_inches='tight')
