#!/usr/bin/env python

import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np

n_cum_time = "Accumulated Time (ms)"
n_pos = "# Rendered Views"

figure_pattern = "{}_fig.pdf"

def single_plot(filename, batch_time):
    df = pd.read_csv(filename)

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
    f.savefig(figure_pattern.format(filename), bbox_inches='tight')


if __name__ == "__main__":
    # The processed picto results file
    filename = sys.argv[1]
    # The time it took the batch M2T transformation to complete
    batch_time = float(sys.argv[2])

    # or

    # filename = "../models/comps.ecore.profiling.csv"
    # batch_time = 250
    single_plot(filename, batch_time)
