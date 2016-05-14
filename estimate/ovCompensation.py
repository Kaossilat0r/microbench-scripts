'''
Created on 29.10.2015

@author: roman
'''

import matplotlib as mpl
import numpy as np

from estimate import jsonData
from estimate import constants as C

mpl.use('pgf')
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
def new_fig(width):
    plt.clf()
    fig = plt.figure(figsize=size_of_figure(width))
    ax = fig.add_subplot(111)
    plt.gcf().subplots_adjust(bottom=0.20)  # show x label
    # 	plt.gcf().subplots_adjust(left=0.15)	# show y label

    # 	ax.set_axisbelow(True)

    # 	ax.set_ylim([0,800])	# MAX Y
    # 	ax.yaxis.set_ticks([1,5,10,15,20])	# x axis labels 1,2,3,...,10

    # 	ax.xaxis.set_ticks(np.arange(1, 11, 1))	# x axis labels 1,2,3,...,10

    return fig, ax


def save_fig(filename):
    print('saving {}'.format(filename))
    # plt.savefig('../{}.pgf'.format(filename))
    plt.savefig('../{}.pdf'.format(filename))

if __name__ == '__main__':
    # Simple plot
    fig, ax = new_fig(1.0)

    data = jsonData.parse_benchmark_results('../spec-output-stats')

    # refValues, afterOvCompensation, beforeOvCompensation, names = [],[],[],[]
    names, values = [], {C.REF: [], C.COMP: [], C.PROF: []}
    for v in data:
        names.append(v[C.NAME])
        values[C.PROF].append(v[C.PROF])
        values[C.COMP].append(v[C.COMP])
        values[C.REF].append(v[C.REF])

    print(values)

    ind = np.arange(len(names))  # the x locations for the groups
    bar_width = 0.5  # the width of the bars: can also be len(x) sequence

    pBefore = plt.bar(ind, values[C.PROF], bar_width, color='y', zorder=3)
    pAfter = plt.bar(ind, values[C.COMP], bar_width, color='r', zorder=3)
    pRef = plt.bar(ind, values[C.REF], bar_width, color='b', zorder=3)

    plt.xticks(ind + bar_width / 2., names, rotation=25)
    # plt.yticks(np.arange(0, max(values['profileTime']), 500))
    plt.legend((pBefore, pAfter, pRef),
               ('w/o ovCompensation', 'w/ ovCompensation', 'ref runtime'), loc="upper right")

    plt.grid(True, zorder=0, axis='y')
    plt.ylabel("runtime [s]")

    outName = "outName"
    save_fig(outName)

    # second figure
    fig, ax = new_fig(1.0)
    save_fig("second")