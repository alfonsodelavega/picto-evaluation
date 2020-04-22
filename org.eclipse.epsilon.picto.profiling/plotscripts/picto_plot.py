#!/usr/bin/env python
# Usage: ./picto_plot.py <profiling_csv_file> <time_for_batch_processing>
# Example: ./picto_plot.py comps.ecore.profiling.csv 600

#%%
import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np

#%%
n_element = "Element"
n_time = "TimeMillis"
n_avg_time = "AvgTimeMillis"
n_std_time = "StdTimeMillis"
n_views_avg = "AvgAcrossviews"
n_cum_time = "Accumulated Time (ms)"
n_treeViewer_row = "TreeViewer"
n_pos = "# Rendered Views"

# The profiling file
filename = sys.argv[1]
# The time it took the batch M2T transformation to complete (used in plot below)
batch_time = float(sys.argv[2])

# or

# filename = "../models/comps.ecore.profiling.csv"
# batch_time = 250

df = pd.read_csv(filename)
df

#%%
#TODO: Decide if it is necessary to remove best/worst obtained time

df = df.groupby([n_element])[n_time].agg(["mean", "std"]).reset_index()
df.columns = [n_element, n_avg_time, n_std_time]
df

#%%

# x axis position
# The tree viewer time should be the axis 0 value
# (not sure about the order of the others, alphanumeric atm)
#TODO: decide order of rendered views
df[n_pos] = df.index + 1
df.set_index(n_element, inplace=True)
df.at[n_treeViewer_row, n_pos] = 0
df.sort_values(by=[n_pos], inplace=True)
df

# %%
# Average view rendering times to get a uniform graph
df[n_views_avg] = df[n_avg_time].mean()

# Get accumulated times as new views are rendered
df[n_cum_time] = df[n_views_avg].cumsum()
df

# %%
# Plot
f, ax = plt.subplots(1)

ax.plot((0, df[n_pos].iat[-1]), (batch_time, batch_time), "red")
ax.plot(df[n_pos], df[n_cum_time],
        linestyle='-', marker='o', color='b')
ax.set_ylim(bottom=0)
ax.set_xlim([0, df[n_pos].iat[-1]])
ax.set_xlabel(n_pos)
ax.set_ylabel(n_cum_time)
#plt.xticks(np.arange(0, df[n_pos].iat[-1]+1, 1))
#plt.show()
f.savefig("{}_fig.pdf".format(filename), bbox_inches='tight')
df_processed = df[[n_pos, n_avg_time, n_std_time, n_views_avg, n_cum_time]]
df_processed.to_csv("{}_processed.csv".format(filename), index=True)

print("Saved processed csv in {}_processed.csv".format(filename))
print("Saved figure in {}_fig.pdf".format(filename))
