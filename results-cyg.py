
'''
2015-04
A script to parse the micro benchmark results and generate graphs
@author: roman
'''
from sys import argv
import ntpath #basename
import math
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
		if not len(cols) == 15:
			continue
		
		try:
			depth = int(cols[0])
		except ValueError:
			continue
		
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
			scatterScale = val[e]*(10000*math.sqrt(scaleFactor)/datas)	# size of scatter points
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

	plt.savefig("out/{}-{}.png".format(outName, namePostfix))
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
	mins, avgs, datas = {}, {}, 0
	for key, val in nanoDict.items():
		mins[key] = min(val.keys())
		
		sums = 0
		for t, amount in val.items():
			sums += t * amount
		avg = sums / sum(val.values())
		avgs[key] = round(avg)
		
		datas += sum(val.values())
		
	# dump
	logFile = open("./out/log.txt", "w")
	logFile.write(str(microDict))
	logFile.close()
	
	infoFile = open("./out/{}.txt".format(outName), "w")
	infoFile.write("{} - {} samples".format(outName, datas) + "\n")
	for key in nanoDict.keys():
		diff = avgs[key]-mins[key]
		diffProc = round(diff/mins[key]*100*100)/100
		infoFile.write("{:>3} - mean: {:>7} - min: {:>7} - diff: {:>5} ({:>4}%)".format(key, avgs[key], mins[key], diff, diffProc) + "\n")
	infoFile.close()
	
	#graph	
	print("Creating graphs ..")
	generateGraph(nanoDict, 1000, "nanos")
	generateGraph(microDict, 1, "micros")
