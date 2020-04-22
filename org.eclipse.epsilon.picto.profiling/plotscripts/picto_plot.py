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
n_cum_time = "AccumulatedTimeMillis"
n_treeViewer_row = "TreeViewer"
n_pos = "# Rendered Views"

filename = sys.argv[1] if len(sys.argv) > 1 else "models/comps.ecore.profiling.csv"

# The time it took the batch M2T transformation to complete (used in plot below)
batch_time = float(sys.argv[2]) if len(sys.argv) > 2 else 600

df = pd.read_csv(filename)
print(df.head())

#%%

#TODO: Decide if it is necessary to remove best/worst obtained time
df = df.groupby([n_element])[n_time].mean().reset_index()

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
# Get accumulated times as new views are rendered
df[n_cum_time] = df[n_time].cumsum()
df

# %%
# Plot
f, ax = plt.subplots(1)

ax.plot(df[n_pos], df[n_cum_time],
         linestyle='-', color='b')
ax.plot((0, df[n_pos].iat[-1]), (batch_time, batch_time), "red")
ax.set_ylim(bottom=0)
ax.set_xlim([0, df[n_pos].iat[-1]])
ax.set_xlabel(n_pos)
ax.set_ylabel("Accumulated Time (ms)")
# plt.xticks(np.arange(0, df[n_pos].iat[-1]+1, 1))
plt.show()
f.savefig("{}_fig.pdf".format(filename), bbox_inches='tight')
df_processed = df[[n_pos, n_time, n_cum_time]]
df_processed.to_csv("{}_processed.csv".format(filename), index=True)
