
'''
2015-04
A script to parse the micro benchmark results and generate graphs
@author: roman

'''

import matplotlib.pyplot as plt

if __name__ == '__main__':
	dict = dict()

	# parse result
# 	inFile = open("./data/synth.out", "r")
	inFile = open("./data/libquantum.out", "r")
	for line in inFile.readlines():
		
		cols = line.split()
		
		if "ref" in line:
			ref = float(cols[2])*1000
			continue
		if not len(cols) == 15:
			continue
		
		try:
			depth = int(cols[0])
		except ValueError:
			continue
		
		runtime = float(cols[2])*1000 - ref
	
		if not depth in dict:
			dict[depth] = {}
	
		if not runtime in dict[depth]:
			dict[depth][runtime] = 1
		else:
			oldVal = dict[depth][runtime]
			dict[depth][runtime] = oldVal + 1
	
	inFile.close()
	
	# dump
	outFile = open("./out", "w")
	outFile.write(str(dict))
	outFile.close()
	
	# avg + min
	mins, avgs, datas = {}, {}, 0
	for key, val in dict.items():
		mins[key] = min(val.keys())
		
		sums = 0
		for t, amount in val.items():
			sums += t * amount
		avg = sums / sum(val.values())
		avgs[key] = avg
		
		datas += sum(val.values())
		
	
	#graph	
	maxKey = max(dict.keys())
	maxTime = 0
	for key, val in dict.items():
		localMax = max(val.keys())
		if localMax > maxTime:
			maxTime = localMax
			
	plt.grid(True)
	plt.show
	
	for key, val in dict.items():
		for e in val:
	#		if e < 2*avgs[key]:
			plt.scatter(key, e, s=val[e]*(50000/datas), alpha=0.3, edgecolors='none')
			
		# avg + min
		mean = plt.scatter(key, avgs[key], c="red", s=10, edgecolors='none', label="mean")
		min = plt.scatter(key, mins[key], c="green", s=10,edgecolors='none', label="min")
			
	plt.xlabel("number of unwinds")
	plt.ylabel('runtime [us]')
	
	plt.legend((mean, min), ("mean", "min"), loc="lower right")
#	plt.axis([0,maxKey+0.5,0,maxTime])	#xmin,xmax,ymin,ymax
	plt.axis([0,maxKey+0.5,0,0.011])	#xmin,xmax,ymin,ymax
	
	plt.savefig('scatter.png')
	plt.savefig('scatter.pdf')
