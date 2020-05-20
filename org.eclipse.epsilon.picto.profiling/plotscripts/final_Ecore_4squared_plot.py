#!/usr/bin/env python
# Usage:
# ./final_Ecore_4squared_plot.py

# This script both processes the raw csv files from the batch and picto
# executions, and generates a single plot that contains all model graphs

#%%
import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
from process_batch_results import process_batch_results, processed_pattern, n_element
from process_picto_results import process_picto_results, n_pos, n_avg_time, n_cum_time

profiling_pattern = "{}.profiling.csv"
plot_output = "../renderEcoreSquared.pdf"

save_intermediate_results = True  # True: saves processed csvs

batch_file = "../batchRenderEcore.csv"
batch_parallel_file = "../batchRenderEcoreParallel.csv"
models_folder = "../models/ecore/"

models = ['UML.ecore', 'CIM15.ecore',
          'GluemodelEmoflonTTC2017.ecore', "RevEngSirius.ecore"]
models_title = {'Ecore.ecore' : "Ecore.ecore" ,
                'UML.ecore' : "UML.ecore",
                'CIM15.ecore' : "CIM.ecore",
                'GluemodelEmoflonTTC2017.ecore' : "EmoflonTTC17.ecore",
                "RevEngSirius.ecore" : "RevEngSirius.ecore"}


#%%
df_batch = process_batch_results(batch_file)
df_batch_parallel = process_batch_results(batch_parallel_file)
if save_intermediate_results:
    df_batch.to_csv(processed_pattern.format(batch_file),
                    index=False)
    df_batch_parallel.to_csv(processed_pattern.format(batch_parallel_file),
                                index=False)


#%%
plt.style.use('seaborn-white')

plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{libertine}')
plt.rc("font", family="serif")

SMALL_SIZE = 18
MEDIUM_SIZE = 20

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=22)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize


#%%
f = plt.figure(figsize=(8,10))
axes = f.subplots(nrows=2, ncols=2)


for model, ax in zip(models, [ax for axes_row in axes for ax in axes_row]):
    batch_time = df_batch[ df_batch[n_element] == model ][n_avg_time].iloc[0]
    batch_parallel_time = df_batch_parallel[
        df_batch_parallel[n_element] == model ][n_avg_time].iloc[0]

    model_path = models_folder + profiling_pattern.format(model)
    model_df = process_picto_results(model_path)
    if save_intermediate_results:
        model_df.to_csv(processed_pattern.format(model_path), index=True)

    ax.plot((0, model_df[n_pos].iat[-1]),
            (batch_time/1000, batch_time/1000),
            linestyle=":",
            linewidth=2,
            color="#cc3311",
            label="sThread")
    ax.plot((0, model_df[n_pos].iat[-1]),
            (batch_parallel_time/1000, batch_parallel_time/1000),
            linestyle="--",
            linewidth=2,
            color="#117733",
            label="mThread")
    ax.plot(model_df[n_pos],
            model_df[n_cum_time]/1000,
            linestyle='-',
            linewidth=2,
            color='#0077bb',
            label="Vista")
    ax.set_ylim(bottom=0)
    ax.set_xlim([0, model_df[n_pos].iat[-1]])
    ax.set_title(models_title[model])
    ax.legend()


yTitle = "Accumulated time (s)"
xTitle = "\# Opened views"

axes[0,0].set_ylabel(yTitle)
axes[1,0].set_ylabel(yTitle)
axes[1,0].set_xlabel(xTitle)
axes[1,1].set_xlabel(xTitle)

#%%
f.tight_layout()
f.savefig(plot_output, bbox_inches='tight')
