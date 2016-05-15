"""
Created on 29.10.2015

@author: roman
"""

import os

import matplotlib as mpl
import numpy as np

from estimate import jsonData
from estimate import constants as C

mpl.use('pgf')  # has to be set before the following import
import matplotlib.pyplot as plt


def size_of_figure(scale):
    fig_width_pt = 497.92325  # Get this from LaTeX using \the\textwidth
    inches_per_pt = 1.0 / 72.27  # Convert pt to inch
    # 	golden_mean = (np.sqrt(5.0)-1.0)/2.0            # Aesthetic ratio (you could change this)
    golden_mean = 1 / 3  # Aesthetic ratio (you could change this)
    fig_width = fig_width_pt * inches_per_pt * scale  # width in inches
    fig_height = fig_width * golden_mean  # height in inches
    fig_size = [fig_width, fig_height]
    return fig_size


defaultLineWidth = 0.4

pgf_with_latex = {  # setup matplotlib to use latex for output
    "pgf.texsystem": "pdflatex",  # change this if using xetex or lautex
    "text.usetex": True,  # use LaTeX to write all text
    "font.family": "serif",
    "font.serif": [],  # blank entries should cause plots to inherit fonts from the document
    "font.sans-serif": [],
    "font.monospace": [],
    "axes.labelsize": 10,  # LaTeX default is 10pt font.
    "font.size": 10,
    "legend.fontsize": 8,  # Make the legend/label fonts a little smaller
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "figure.figsize": size_of_figure(0.9),  # default fig size of 0.9 textwidth

    "lines.linewidth": defaultLineWidth,  # line width of means
    "axes.linewidth": defaultLineWidth,  # line width of

    "pgf.preamble": [
        r"\usepackage[utf8x]{inputenc}",  # use utf8 fonts becasue your computer can handle it :)
        r"\usepackage[T1]{fontenc}",  # plots will be generated using this preamble
    ]
}
mpl.rcParams.update(pgf_with_latex)


# I make my own newfig and savefig functions
def new_fig(width, max_y=0):
    plt.clf()
    fig = plt.figure(figsize=size_of_figure(width))
    ax = fig.add_subplot(111)
    plt.gcf().subplots_adjust(bottom=0.20)  # show x label
    plt.gcf().subplots_adjust(left=0.15)    # show y label

    # 	ax.set_axisbelow(True)

    if max_y:
        ax.set_ylim([0, max_y]) # MAX Y
    # 	ax.yaxis.set_ticks([1,5,10,15,20])	# x axis labels 1,2,3,...,10

    # 	ax.xaxis.set_ticks(np.arange(1, 11, 1))	# x axis labels 1,2,3,...,10

    return fig, ax


def save_fig(filename):
    print('saving {}'.format(filename))
    # plt.savefig('../{}/{}.pgf'.format(C.OUT_DIR, filename))
    plt.savefig('../{}/{}.pdf'.format(C.OUT_DIR, filename))


def figure_ov_compensation():
    fig, ax = new_fig(1.0)

    names, values = [], {C.REF: [], C.COMP: [], C.PROF: []}
    for v in ov_compensation_data:
        names.append(v[C.NAME])
        values[C.PROF].append(v[C.PROF])
        values[C.COMP].append(v[C.COMP])
        values[C.REF].append(v[C.REF])

    ind = np.arange(len(names))  # the x locations for the groups
    bar_width = 0.5  # the width of the bars: can also be len(x) sequence
    p_before = plt.bar(ind, values[C.PROF], bar_width, color='y', zorder=3)
    p_after = plt.bar(ind, values[C.COMP], bar_width, color='r', zorder=3)
    p_ref = plt.bar(ind, values[C.REF], bar_width, color='b', zorder=3)
    plt.xticks(ind + bar_width / 2., names, rotation=25)
    plt.legend((p_before, p_after, p_ref),
               ('w/o ovCompensation', 'w/ ovCompensation', 'ref runtime'), loc="upper right")
    plt.grid(True, zorder=0, axis='y')
    plt.ylabel("runtime [s]")
    save_fig("overheadCompensation")


def figure_single_benchmark():

    for benchmark in ov_compensation_data:
        fig, ax = new_fig(1.0)

        benchmark_name = benchmark[C.NAME]
        phase_names, ov_percents = [], {C.INSTR_PERCENT: [], C.UNW_PERCENT: []}
        for name in C.PHASE_ORDER:
        # for name, v in sorted(benchmark[C.PHASES].items()):
            v = benchmark[C.PHASES][name]
            if v[C.INSTR_PERCENT] + v[C.UNW_PERCENT] > 0:
                phase_names.append(C.PN[name])
                ov_percents[C.INSTR_PERCENT].append(v[C.INSTR_PERCENT])
                ov_percents[C.UNW_PERCENT].append(v[C.UNW_PERCENT])

        ind = np.arange(0.25, len(phase_names)+0.25)  # the x locations for the groups
        bar_width = 0.5  # the width of the bars: can also be len(x) sequence
        p_instr = plt.bar(ind, ov_percents[C.INSTR_PERCENT], bar_width, color='b', zorder=3)
        p_unw = plt.bar(ind, ov_percents[C.UNW_PERCENT], bar_width, color='r', zorder=3, bottom=ov_percents[C.INSTR_PERCENT])
        plt.xticks(ind + bar_width / 2., phase_names, rotation=25)
        plt.legend((p_unw, p_instr),
                   ('unwind ', 'instrumentation'), loc="upper right")
        plt.grid(True, zorder=0, axis='y')
        plt.ylabel("overhead [%]")
        save_fig(benchmark_name)


def figure_single_phase():

    for phase_name in C.PHASE_ORDER:
        fig, ax = new_fig(1.0)

        phase_display_name = C.PN[phase_name]
        names, values = [], {C.INSTR_PERCENT: [], C.UNW_PERCENT: [], C.PERCENT: []}
        for benchmark in ov_compensation_data:
            names.append(benchmark[C.NAME])

            ov_data = benchmark[C.PHASES][phase_name]
            values[C.INSTR_PERCENT].append(ov_data[C.INSTR_PERCENT])
            values[C.UNW_PERCENT].append(ov_data[C.UNW_PERCENT])
            values[C.PERCENT].append(ov_data[C.PERCENT])

        ind = np.arange(0.25, len(names) + 0.25)  # the x locations for the groups
        bar_width = 0.5  # the width of the bars: can also be len(x) sequence
        p_instr = plt.bar(ind, values[C.INSTR_PERCENT], bar_width, color='b', zorder=3)
        p_unw = plt.bar(ind, values[C.UNW_PERCENT], bar_width, color='r', zorder=3,
                        bottom=values[C.INSTR_PERCENT])
        plt.xticks(ind + bar_width / 2., names, rotation=25)
        plt.legend((p_unw, p_instr),
                   ('unwind ', 'instrumentation'), loc="upper right")
        plt.grid(True, zorder=0, axis='y')
        plt.ylabel("overhead [%]")
        save_fig(phase_display_name)


if __name__ == '__main__':

    if not os.path.exists(C.OUT_DIR):
        os.makedirs(C.OUT_DIR)

    ov_compensation_data = jsonData.parse_benchmark_results('../spec-output-stats')

    figure_ov_compensation()

    # figure_single_benchmark()

    figure_single_phase()
