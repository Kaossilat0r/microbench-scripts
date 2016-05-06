
'''
2015-04
A script to parse the micro benchmark results and generate graphs
@author: roman
'''
from sys import argv
import ntpath #basename
import math
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
    "pgf.preamble": [
        r"\usepackage[utf8x]{inputenc}",    # use utf8 fonts becasue your computer can handle it :)
        r"\usepackage[T1]{fontenc}",        # plots will be generated using this preamble
        ]
    }
mpl.rcParams.update(pgf_with_latex)

import matplotlib.pyplot as plt

def stringToNanos(s):
	return round(float(s)*1000*1000*1000)

def parseNanoDict():

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
	
		if not depth in nanoDict:
			nanoDict[depth] = {}
	
		if not runtime in nanoDict[depth]:
			nanoDict[depth][runtime] = 1
		else:
			oldVal = nanoDict[depth][runtime]
			nanoDict[depth][runtime] = oldVal + 1
	
	inFile.close()

def convertToMicroDict():
	for depth, times in nanoDict.items():
		microDict[depth] = {}
		for rtime, amount in times.items():
			microTime = round(rtime/1000)
			if not microTime in microDict[depth]:
				microDict[depth][microTime] = 0
			microDict[depth][microTime] = microDict[depth][microTime] + amount

def generateGraph(theDict, scaleFactor, namePostfix):
	maxKey = max(theDict.keys())
	maxTime = 0
	for key, val in theDict.items():
		localMax = max(val.keys())
		if localMax > maxTime:
			maxTime = localMax
			
	plt.grid(True, zorder=0)
	plt.show
	
	for key, val in theDict.items():
		for e in val:
			scatterScale = val[e]*(10000*math.sqrt(scaleFactor)/numSamples)	# size of scatter points
#			plt.scatter(key, e/scaleFactor, s=scatterScale, alpha=0.3, edgecolors='none')
			plt.scatter(key, e/scaleFactor, s=scatterScale, marker="_")
			
		# avg + min
		mean = plt.scatter(key, avgs[key]/1000, c="red", s=100, marker="_", edgecolors="red", label="mean")
		min = plt.scatter(key, mins[key]/1000, c="green", s=100, marker="_", label="min")
			
	plt.xlabel("number of unwinds")
	plt.ylabel("runtime [us]")
	
	plt.legend((mean, min), ("mean", "min"), loc="upper left")
	plt.axis([0,maxKey+0.5,0,maxTime/scaleFactor])	#xmin,xmax,ymin,ymax
#	plt.axis([0,maxKey+0.5,0,0.011])	#xmin,xmax,ymin,ymax

# 	plt.savefig("out/{}-{}.png".format(outName, namePostfix))
# 	plt.savefig("out/{}-{}.pdf".format(outName, namePostfix))
	plt.savefig("out/{}-{}.pgf".format(outName, namePostfix))
	plt.savefig("out/{}-{}.pdf".format(outName, namePostfix))
	
	plt.close()
	
	print("Saved graph to out/{}-{}.png".format(outName, namePostfix))

if __name__ == '__main__':
	
	if(len(argv)>1):
		inName = argv[1]
	else:
		inName = "./in/synth-nocache.out"
	outName = ntpath.basename(inName).split(".")[0]
	
	nanoDict = dict()
	parseNanoDict()
	print("Created nano dict.")
	
	microDict = dict()
	convertToMicroDict()
	print("Created micro dict.")
	
	# avg + min
	mins, maxs, avgs, numSamples = {}, {}, {}, 0
	for key, val in nanoDict.items():
		mins[key] = min(val.keys())
		maxs[key] = max(val.keys())
		
		sums = 0
		for t, amount in val.items():
			sums += t * amount
		avg = sums / sum(val.values())
		avgs[key] = round(avg)
		
		numSamples += sum(val.values())
		
	# dump
	logFile = open("./out/{}.dump".format(outName), "w")
	logFile.write(str(microDict))
	logFile.close()
	
	infoFile = open("./out/{}.txt".format(outName), "w")
	infoFile.write("{} - {} samples".format(outName, numSamples) + "\n")
	infoFile.write("#unw | mean[ns] | min[ns] | diffmin[ns](-%) | max[ns] | diffmax[ns]    (+%)" + "\n")
	for key in nanoDict.keys():
		diffMin = avgs[key]-mins[key]
		diffMinProc = round(diffMin/avgs[key]*100*100)/100
		diffMax = maxs[key]-avgs[key]
		diffMaxProc = round(diffMax/avgs[key]*100*100)/100
		infoFile.write("{:>4} | {:>8} | {:>7} | {:>6} (-{:>4}%) | {:7} | {:>7} (+{:>7}%) ".format(key, avgs[key], mins[key], diffMin, diffMinProc, maxs[key], diffMax, diffMaxProc) + "\n")
	infoFile.close()
	
	#graph	
	
	print("Creating graphs ..")
	generateGraph(nanoDict, 1000, "nanos")
	generateGraph(microDict, 1, "micros")
