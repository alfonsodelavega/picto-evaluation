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


save_intermediate_results = True  # True: saves processed csvs

if len(sys.argv) > 1:
    batch_file = sys.argv[1]
    batch_parallel_file = sys.argv[2]
    models_folder = sys.argv[3]
    plot_output = "{}/renderGenComps2Models.pdf".format(models_folder)
    data_output = "{}/renderGenComps2Models-data.txt".format(models_folder)
else:
    batch_file = "../batchRenderGenComps.csv"
    batch_parallel_file = "../batchRenderGenCompsParallel.csv"
    models_folder = "../models/gencomps/"
    plot_output = "../renderGenComps2Models.pdf"
    data_output = "../renderGenComps2Models-data.txt"

models = ['gencomps-12.9K.model', "gencomps-29K.model"]
models_title = {'Ecore.ecore' : "Ecore.ecore" ,
                'gencomps-01.5K.model' : "gencomps-01.5K.model",
                'gencomps-05.8K.model' : "gencomps-05.8K.model",
                'gencomps-12.9K.model' : "gencomps-12.9K.model",
                "gencomps-29K.model" : "gencomps-29K.model"}

model2single = {}
model2parallel = {}
model2pictoresults = {}

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
plt.rc('text.latex',
       preamble=r'\usepackage{libertine} \newcommand{\picto}{\textsc{Vista}}')
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
f = plt.figure(figsize=(8,4))
axes = f.subplots(nrows=1, ncols=2)


for model, ax in zip(models, [ax for ax in axes]):
    batch_time = df_batch[ df_batch[n_element] == model ][n_avg_time].iloc[0]
    batch_parallel_time = df_batch_parallel[
        df_batch_parallel[n_element] == model ][n_avg_time].iloc[0]

    model_path = models_folder + profiling_pattern.format(model)
    model_df = process_picto_results(model_path)

    # convert to seconds
    batch_time = batch_time / 1000
    batch_parallel_time = batch_parallel_time / 1000
    model_df[n_cum_time] = model_df[n_cum_time] / 1000

    # save this for later
    model2single[model] = batch_time
    model2parallel[model] = batch_parallel_time
    model2pictoresults[model] = model_df

    if save_intermediate_results:
        model_df.to_csv(processed_pattern.format(model_path), index=True)

    ax.plot((0, model_df[n_pos].iat[-1]),
            (batch_time, batch_time),
            linestyle=":",
            linewidth=2,
            color="#cc3311",
            label="single-thread")
    ax.plot((0, model_df[n_pos].iat[-1]),
            (batch_parallel_time, batch_parallel_time),
            linestyle="--",
            linewidth=2,
            color="#117733",
            label="multi-thread")
    ax.plot(model_df[n_pos],
            model_df[n_cum_time],
            linestyle='-',
            linewidth=2,
            color='#0077bb',
            label="\picto")
    ax.set_ylim(bottom=0)
    ax.set_xlim([0, model_df[n_pos].iat[-1]])
    ax.set_title(models_title[model])

# stacked axis titles
yTitle = "Accumulated time (s)"
xTitle = "\# Opened views"

axes[0].set_ylabel(yTitle)
axes[0].set_xlabel(xTitle)
axes[1].set_xlabel(xTitle)

# axis ticks fixes


# bottom legend
handles, labels = axes[1].get_legend_handles_labels()
f.legend(handles, labels, frameon=False, ncol=3,
         loc='lower center', bbox_to_anchor=(0.5,-0.04))

#%%
f.tight_layout()
f.savefig(plot_output, bbox_inches='tight')

#%%
# print both to stdout and to file f
def printb(string, f):
    print(string)
    print(string, file=f)

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


#%%
'''
Calculation of numbers needed in the paper:
'''

f = open(data_output, "w")

for model in models:
    printb(model, f)
    single = model2single[model]
    multi = model2parallel[model]
    picto_df = model2pictoresults[model]

    # Total number of views
    num_views = picto_df[n_pos].iat[-1]
    printb("\tTotal number of views: {}".format(num_views), f)
    printb("", f)

    # Final time for each solution
    picto_total_time = picto_df[n_cum_time].iat[-1]
    printb("\tSingle-thread time: {}".format(single), f)
    printb("\tMulti-thread time: {}".format(multi), f)
    printb("\tPicto total time: {}".format(picto_total_time), f)
    printb("", f)

    # multi vs single-thread (time savings)
    multi_thread_improvement = (single - multi) / single
    printb("\tMulti vs single thread time savings: {}".format(multi_thread_improvement), f)
    printb("", f)

    # Overhead (picto - singlethread)
    picto_overhead = (picto_total_time - single) / picto_total_time
    printb("\tPicto time overhead against single: {}".format(picto_overhead), f)
    printb("", f)

    # crossings
    picto_line = [[0, picto_df[n_cum_time].iat[0]],
                  [num_views, picto_total_time]]
    single_line = [[0, single], [num_views, single]]
    multi_line = [[0, multi], [num_views, multi]]

    multi_views, _ = line_intersection(picto_line, multi_line)
    single_views, _ = line_intersection(picto_line, single_line)

    printb("\tMulti-thread crossing:", f)
    printb("\t\tCrossing views: {}".format(multi_views), f)
    printb("\t\tCrossing views(%): {}".format(100*multi_views/num_views), f)
    printb("", f)

    printb("\tSingle-thread crossing:", f)
    printb("\t\tCrossing views: {}".format(single_views), f)
    printb("\t\tCrossing views(%): {}".format(100*single_views/num_views), f)
    printb("", f)

    printb("", f)

f.close()
