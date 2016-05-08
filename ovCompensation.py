'''
Created on 29.10.2015

@author: roman
'''

from sys import argv
import ntpath #basename

import numpy as np
import matplotlib as mpl
mpl.use('pgf')

def figsize(scale):
	fig_width_pt = 497.92325                         # Get this from LaTeX using \the\textwidth
	inches_per_pt = 1.0/72.27                       # Convert pt to inch
# 	golden_mean = (np.sqrt(5.0)-1.0)/2.0            # Aesthetic ratio (you could change this)
	golden_mean = 1/3           # Aesthetic ratio (you could change this)
	fig_width = fig_width_pt*inches_per_pt*scale    # width in inches
	fig_height = fig_width*golden_mean              # height in inches
	fig_size = [fig_width,fig_height]
	return fig_size

defaultLineWidth = 0.4

pgf_with_latex = {                      # setup matplotlib to use latex for output
    "pgf.texsystem": "pdflatex",        # change this if using xetex or lautex
    "text.usetex": True,                # use LaTeX to write all text
    "font.family": "serif",
    "font.serif": [],                   # blank entries should cause plots to inherit fonts from the document
    "font.sans-serif": [],
    "font.monospace": [],
    "axes.labelsize": 10,               # LaTeX default is 10pt font.
    "font.size": 10,
    "legend.fontsize": 8,               # Make the legend/label fonts a little smaller
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "figure.figsize": figsize(0.9),     # default fig size of 0.9 textwidth
    
    "lines.linewidth": defaultLineWidth,				# line width of means
    "axes.linewidth": defaultLineWidth,				# line width of
    
    "pgf.preamble": [
        r"\usepackage[utf8x]{inputenc}",    # use utf8 fonts becasue your computer can handle it :)
        r"\usepackage[T1]{fontenc}",        # plots will be generated using this preamble
        ]
    }
mpl.rcParams.update(pgf_with_latex)

import matplotlib.pyplot as plt

# I make my own newfig and savefig functions
def newfig(width):
	plt.clf()
	fig = plt.figure(figsize=figsize(width))
	ax = fig.add_subplot(111)
	plt.gcf().subplots_adjust(bottom=0.20)	# show x label
# 	plt.gcf().subplots_adjust(left=0.15)	# show y label
	
# 	ax.set_axisbelow(True)
	
# 	ax.set_ylim([0,800])	# MAX Y
# 	ax.yaxis.set_ticks([1,5,10,15,20])	# x axis labels 1,2,3,...,10
	
# 	ax.xaxis.set_ticks(np.arange(1, 11, 1))	# x axis labels 1,2,3,...,10
	
	return fig, ax

def savefig(filename):
	print('saving {}'.format(filename))
#	plt.savefig('{}.pgf'.format(filename))
	plt.savefig('{}.pdf'.format(filename))


# Simple plot
fig, ax  = newfig(1.0)

data = {
	'403.gcc' : {'refTime' : 40.3, 'ovCompTime' : 166.825, 'profileTime' : 661},
	'429.mcf' : {'refTime' : 236.2, 'ovCompTime' : 418.543, 'profileTime' : 1901},
	'433.milc' : {'refTime' : 421.7, 'ovCompTime' : 639.526, 'profileTime' : 2041},
	'444.namd' : {'refTime' : 425.7, 'ovCompTime' : 494.275, 'profileTime' : 2227},
	'447.dealII' : {'refTime' : 26.5, 'ovCompTime' : 4307.31, 'profileTime' : 17483},
	'450.soplex' : {'refTime' : 102.9, 'ovCompTime' : 781.799, 'profileTime' : 11003},
	'453.povray' : {'refTime' : 166.6, 'ovCompTime' : 2733.38, 'profileTime' : 16734},
	'456.hmmer' : {'refTime' : 332.9, 'ovCompTime' : 346.791, 'profileTime' : 523},
	'458.sjeng' : {'refTime' : 509.9, 'ovCompTime' : 1831.16, 'profileTime' : 7446},
	'462.libquantum' : {'refTime' : 402.8, 'ovCompTime' : 424.877, 'profileTime' : 724},
	'464.h264ref' : {'refTime' : 71.2, 'ovCompTime' : 146.955, 'profileTime' : 1430},
	'470.lbm' : {'refTime' : 365.7, 'ovCompTime' : 366, 'profileTime' : 366},
	'473.astar' : {'refTime' : 157.1, 'ovCompTime' : 604.128, 'profileTime' : 6056},
	'482.sphinx3' : {'refTime' : 535.2, 'ovCompTime' : 672.739, 'profileTime' : 2149}
	}

# refValues, afterOvCompensation, beforeOvCompensation, names = [],[],[],[]
names, values = [], {'refTime':[], 'ovCompTime':[], 'profileTime':[]}
for k, v in sorted(data.items()):
	names.append(k)
	for k2, v2 in v.items():
		values[k2].append(v2)
		
print(values)

ind = np.arange(len(names))    # the x locations for the groups
width = 0.5       # the width of the bars: can also be len(x) sequence

pBefore = plt.bar(ind, values['profileTime'], width, color='y', bottom=0)
pAfter = plt.bar(ind, values['ovCompTime'], width, color='r')
pRef = plt.bar(ind, values['refTime'], width, color='b')

plt.xticks(ind + width/2., names, rotation=25)
# plt.yticks(np.arange(0, max(values['profileTime']), 500))
plt.legend((pBefore[0], pAfter[0], pRef[0]), 
		('w/o ovCompensation', 'w/ ovCompensation', 'ref runtime'), loc="upper right")

plt.show()

plt.grid(True, zorder=5, axis='y')
plt.ylabel("runtime [s]")



outName = "outName"
savefig(outName)
