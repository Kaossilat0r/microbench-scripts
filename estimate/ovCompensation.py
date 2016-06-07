"""
Created on 29.10.2015

@author: roman
"""

import os

import matplotlib as mpl
import numpy as np

from estimate import jsonData
from estimate import constants as C
from estimate import pgfHack

mpl.use('pgf')  # has to be set before the following import
import matplotlib.pyplot as plt


defaultLineWidth = 1.0
ratio = (np.sqrt(5.0)-1.0)/2.0  # golden mean

def size_of_figure(scale, figure_ratio):
    fig_width_pt = 497.92325  # Get this from LaTeX using \the\textwidth
    inches_per_pt = 1.0 / 72.27  # Convert pt to inch
    fig_width = fig_width_pt * inches_per_pt * scale  # width in inches
    fig_height = fig_width * figure_ratio  # height in inches
    fig_size = [fig_width, fig_height]
    return fig_size


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
    "figure.figsize": size_of_figure(1.0, ratio),  # this is overwritten in new_fig()

    "lines.linewidth": defaultLineWidth,  # line width of means
    "axes.linewidth": defaultLineWidth,  # line width of

    "pgf.preamble": [
        r"\usepackage[utf8x]{inputenc}",  # use utf8 fonts becasue your computer can handle it :)
        r"\usepackage[T1]{fontenc}",  # plots will be generated using this preamble
    ]
}
mpl.rcParams.update(pgf_with_latex)


# I make my own newfig and savefig functions
def new_fig(width, max_y=0, figure_ratio=ratio):
    plt.clf()
    fig = plt.figure(figsize=size_of_figure(width, figure_ratio))
    ax = fig.add_subplot(111)
    plt.gcf().subplots_adjust(bottom=0.20)  # show x label
    plt.gcf().subplots_adjust(top=0.85)  # show title
    plt.gcf().subplots_adjust(left=0.15)    # show y label
    plt.gcf().subplots_adjust(right=0.95)  # show y label

    pgf_with_latex["figure.figsize"] = size_of_figure(width, figure_ratio)
    # 	ax.set_axisbelow(True)

    if max_y:
        ax.set_ylim([0, max_y]) # MAX Y
    # 	ax.yaxis.set_ticks([1,5,10,15,20])	# x axis labels 1,2,3,...,10

    # 	ax.xaxis.set_ticks(np.arange(1, 11, 1))	# x axis labels 1,2,3,...,10

    return fig, ax


def save_fig(filename, fix_pgf=False):
    save_prefix = '../{}{}/{}'.format(rel_thesis_dir, C.OUT_DIR, filename)
    print('saving {}'.format(save_prefix))
    plt.savefig(save_prefix + '.pdf')
    plt.savefig(save_prefix + '.pgf')

    if fix_pgf:
        pgfHack.fix_pgf_file(save_prefix + '.pgf')

def figure_ov_compensation():
    fig, ax = new_fig(1.0, figure_ratio=1/3)

    names, values = [], {C.REF: [], C.COMP: [], C.PROF: []}
    for v in ov_compensation_data_with_avg:
        names.append(v[C.NAME])
        values[C.PROF].append(v[C.PROF])
        values[C.COMP].append(v[C.COMP])
        values[C.REF].append(v[C.REF])

    ind = np.arange(len(names))  # the x locations for the groups
    bar_width = 0.5  # the width of the bars: can also be len(x) sequence
    p_before = plt.bar(ind + 0.25, values[C.PROF], bar_width, color='y', zorder=3)
    p_after = plt.bar(ind + 0.25, values[C.COMP], bar_width, color='r', zorder=3)
    p_ref = plt.bar(ind + 0.25, values[C.REF], bar_width, color='b', zorder=3)
    plt.xticks(ind + bar_width / 2., names, rotation=25)
    plt.legend((p_before, p_after, p_ref),
               ('before ov compensation', 'after ov compensation', 'ref runtime'), loc="upper right")
    plt.grid(True, zorder=0, axis='y')
    plt.ylabel("runtime [s]")
    save_fig("overheadCompensation")
    plt.close()


def figure_single_benchmark(max_y=20):

    for benchmark in ov_compensation_data_with_avg:
        fig, ax = new_fig(0.5)

        benchmark_name = benchmark[C.NAME]
        phase_names, ov_percents = [], {C.INSTR_PERCENT: [], C.UNW_PERCENT: []}
        for name in C.PHASE_ORDER:
            v = benchmark[C.PHASES][name]
            if v[C.INSTR_PERCENT] + v[C.UNW_PERCENT] > 0:
                phase_names.append(name)
                ov_percents[C.INSTR_PERCENT].append(v[C.INSTR_PERCENT])
                ov_percents[C.UNW_PERCENT].append(v[C.UNW_PERCENT])

        ind = np.arange(len(phase_names)) + 0.25  # the x locations for the groups
        bar_width = 0.5  # the width of the bars: can also be len(x) sequence
        p_instr = plt.bar(ind, ov_percents[C.INSTR_PERCENT], bar_width, color='b', zorder=3)
        p_unw = plt.bar(ind, ov_percents[C.UNW_PERCENT], bar_width, color='r', zorder=3, bottom=ov_percents[C.INSTR_PERCENT])

        plt.title(benchmark_name)
        plt.xticks(ind + bar_width / 2., phase_names, rotation=25)
        plt.legend((p_unw, p_instr),
                   ('unw', 'instr'), loc="upper right")
        plt.grid(True, zorder=0, axis='y')
        plt.ylabel(default_y_label)
        save_fig(benchmark_name)

        plt.ylim(0, max_y)
        autolabel(plt, p_unw, above_figure=False)
        autolabel(plt, p_instr, above_figure=False)
        save_fig(benchmark_name + "_" + str(max_y), fix_pgf=True)

        plt.close()

        plt.close()


def figure_single_phase():

    for phase_name in C.PHASE_ORDER:
        fig, ax = new_fig(1.0)

        benchmark_names, values = [], {C.INSTR_PERCENT: [], C.UNW_PERCENT: [], C.PERCENT: []}
        for benchmark in ov_compensation_data_with_avg:
            benchmark_names.append(benchmark[C.NAME])

            ov_data = benchmark[C.PHASES][phase_name]
            values[C.INSTR_PERCENT].append(ov_data[C.INSTR_PERCENT])
            values[C.UNW_PERCENT].append(ov_data[C.UNW_PERCENT])
            values[C.PERCENT].append(ov_data[C.PERCENT])

        ind = np.arange(len(benchmark_names)) + 0.25  # the x locations for the groups
        bar_width = 0.5  # the width of the bars: can also be len(x) sequence
        p_instr = plt.bar(ind, values[C.INSTR_PERCENT], bar_width, color='b', zorder=3)
        p_unw = plt.bar(ind, values[C.UNW_PERCENT], bar_width, color='r', zorder=3,
                        bottom=values[C.INSTR_PERCENT])
        plt.title(phase_name)
        plt.xticks(ind + bar_width/2, benchmark_names, rotation=25)
        plt.legend((p_unw, p_instr),
                   ('unwind ', 'instrumentation'), loc="upper right")
        plt.grid(True, zorder=0, axis='y')
        plt.ylabel(default_y_label)
        save_fig(phase_name)
        plt.close()


def figure_vs_phase(vs_phases_names, max_y=50, fig_width=1.0, fig_ratio=1/3, adjust_bottom=0.20):
    fig, ax = new_fig(fig_width, figure_ratio=fig_ratio)
    plt.gcf().subplots_adjust(top=0.90)  # show title
    plt.gcf().subplots_adjust(bottom=adjust_bottom)  # show x labels
    plt.gcf().subplots_adjust(left=0.07)    # show y label
    plt.gcf().subplots_adjust(right=0.98)

    benchmark_names = []
    for benchmark in ov_compensation_data_with_avg:
        benchmark_names.append(benchmark[C.NAME])

    vs_phases = {}
    for phase_name in vs_phases_names:

        vs_phases[phase_name] = {C.INSTR_PERCENT: [], C.UNW_PERCENT: [], C.PERCENT: []}
        for benchmark in ov_compensation_data_with_avg:
            ov_data = benchmark[C.PHASES][phase_name]
            values = vs_phases[phase_name]
            values[C.INSTR_PERCENT].append(ov_data[C.INSTR_PERCENT])
            values[C.UNW_PERCENT].append(ov_data[C.UNW_PERCENT])
            values[C.PERCENT].append(ov_data[C.PERCENT])

    len_vs = len(vs_phases_names)

    ind = np.arange(len(benchmark_names)) + 0.15  # the x locations for the groups
    bar_width = 0.7 / len_vs  # the width of the bars: can also be len(x) sequence

    offset = 0
    plts = []
    for phase_name in vs_phases_names:
        vs_phase = vs_phases[phase_name]

        p_tmp = plt.bar(ind + offset*bar_width, vs_phase[C.PERCENT], bar_width, color=C.COL[phase_name], zorder=3)
        plts.append(p_tmp)
        offset += 1

    plt.xticks(ind + bar_width*len(vs_phases_names) / 2., benchmark_names, rotation=25)
    plt.legend(plts, vs_phases_names, loc="upper right")
    plt.grid(True, zorder=0, axis='y')
    plt.ylabel(default_y_label)
    filename = ",".join(vs_phases_names)
    save_fig("vs_"+filename)

    plt.ylim(0,max_y)
    for p in plts:
        autolabel(plt, p)
    save_fig("vs_"+filename+"_"+str(max_y), fix_pgf=True)

    plt.close()

    create_latex_table_vs(benchmark_names, filename, vs_phases, vs_phases_names)


def create_latex_table_vs(benchmark_names, filename, vs_phases, vs_phases_names):
    with open("../"+ rel_thesis_table_dir + filename + ".tex", 'w') as out:
        # out.write("\\begin{adjustbox}{max width=\\textwidth,center}\n")
        out.write("\\begin{tabular}{ " + "".join("c" for x in range(len(benchmark_names) + 1)) + " }\n")
        out.write("\\hline\n")
        out.write(" & " + " & ".join("\\rot{" + b.split('.')[1] + "}" for b in benchmark_names) + " \\\\ \\hline\n")
        for phase_name in vs_phases_names:
            out.write(phase_name + " & " + " & ".join(
                "{0:.1f}".format(p) for p in vs_phases[phase_name][C.PERCENT]) + " \\\\\n")
        out.write("\\hline\n")
        out.write("\\end{tabular}\n")
        # out.write("\\end{adjustbox}\n")


def autolabel(plt, rects, above_figure=True):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        if height > plt.ylim()[1]:
            label_x_base = rect.get_x()+rect.get_width()/2.
            if above_figure:
                label_y_base = plt.ylim()[1]*1.05
            else:
                label_y_base = plt.ylim()[1]*0.9
            plt.text(label_x_base, label_y_base, '%d'%int(height), ha='center', va='bottom', color='white', fontsize=8)


if __name__ == '__main__':

    default_y_label = "overhead [\%]"

    if not os.path.exists(C.OUT_DIR):
        os.makedirs(C.OUT_DIR)

    ov_compensation_data, ov_compensation_data_with_avg = jsonData.parse_benchmark_results('../spec-output-stats', consider_sampling_costs=False)
    jsonData.save_file(ov_compensation_data, "../spec-estimation.json")
    jsonData.save_file(ov_compensation_data_with_avg, "../spec-estimation-with-avg.json")

    rel_thesis_dir = "../master-thesis/fig/"
    rel_thesis_table_dir = "../master-thesis/tables/"

    figure_ov_compensation()
    figure_single_benchmark()
    figure_single_phase()

    figure_vs_phase(["ss-all", "unw-all"])    # normal ss vs unw
    figure_vs_phase(["ss-all", "ss-cpd", "unw-all"], max_y=100)    # normal ss vs unw
    figure_vs_phase(["ss-cpd", "ss-min", "ss-conj"], max_y=50)    # optimized ss
    figure_vs_phase(["unw-all", "unw-min"], max_y=50)    # optimized ss
    figure_vs_phase(["ss-cpd", "unw-all", "hybrid"], max_y=50)    # hybrid vs normal
    figure_vs_phase(["ss-cpd", "unw-min", "hybrid-st"], max_y=50) # with structure knowledge only
    figure_vs_phase(["hybrid", "hybrid-st"])
    figure_vs_phase(["ss-min", "unw-min", "hybrid", "hybrid-st"], max_y=50)  # hybrid vs optimized
    figure_vs_phase(['ss-all', 'ss-cpd', 'ss-min', 'ss-conj', 'unw-all', 'unw-min', 'hybrid-st', 'hybrid'],
                    fig_width=1.4, max_y=100, fig_ratio=0.66, adjust_bottom=0.1)
