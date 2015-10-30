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
    fig_width_pt = 469.755                          # Get this from LaTeX using \the\textwidth
    inches_per_pt = 1.0/72.27                       # Convert pt to inch
    golden_mean = (np.sqrt(5.0)-1.0)/2.0            # Aesthetic ratio (you could change this)
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

# parsing stuff
def stringToNanos(s):
	return round(float(s)*1000*1000)

def parseNanoDict(inName):

	print("Parsing data ..")

	inFile = open(inName, "r")
	for line in inFile.readlines():
		
		cols = line.split()
		
		
		if "ref" in line:
			ref = stringToNanos(cols[2])			
			continue
		
		if len(cols) != 19:
			continue
		
		try:
			depth = int(cols[0])
		except ValueError:
			continue

		# do i really want to subtract the reference runtime?		
		runtime = stringToNanos(cols[2]) - ref
		
		if depth == 0:
			continue
		
		data[depth-1].append(runtime)
	
	inFile.close()
	
	print(".. done")

def convertToMicroDict():
	for depth, times in nanoDict.items():
		microDict[depth] = {}
		for rtime, amount in times.items():
			microTime = round(rtime/1000)
			if not microTime in microDict[depth]:
				microDict[depth][microTime] = 0
			microDict[depth][microTime] = microDict[depth][microTime] + amount

# I make my own newfig and savefig functions
def newfig(width):
    plt.clf()
    fig = plt.figure(figsize=figsize(width))
    ax = fig.add_subplot(111)
    plt.gcf().subplots_adjust(bottom=0.15)	# show x label
    
    ax.xaxis.set_ticks(np.arange(1, 11, 1))	# x axis labels 1,2,3,...,10
    
    return fig, ax

def savefig(filename):
	print('saving {}'.format(filename))
	plt.savefig('{}.pgf'.format(filename))
	plt.savefig('{}.pdf'.format(filename))


# Simple plot
fig, ax  = newfig(0.9)

pos = [1,2,3,4,5,6,7,8,9,10]
data = [[] for i in pos]

parseNanoDict(argv[1])

violin_parts = plt.violinplot(dataset=data, positions=pos,points=100, widths=0.9,
                      showmeans=True, showextrema=False, showmedians=False)

for pc in violin_parts['bodies']:
    pc.set_facecolor('green')
    pc.set_edgecolor('green')
    pc.set_linewidths(defaultLineWidth)
    pc.set_alpha(1)
    

#ax.plot(s)
plt.grid(True, zorder=0, axis='y')
plt.xlabel("number of unwinds")
plt.ylabel("runtime [us]")



outName = ntpath.basename(argv[1]).split(".")[0]
savefig(outName)