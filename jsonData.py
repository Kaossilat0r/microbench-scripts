'''
Created on 08.05.2016

@author: roman
'''

import json

def testJson():
	exampleDict = {
		"astar" : {"reftime" : 200, "ovComp" : 250, "PROF" : 500, "phase-instrument" : {"instrOv" : 20, "sampleOv" : 10, "overallOv" : 30} },
		"libquantum" : {"reftime" : 210, "ovComp" : 220, "PROF" : 700},
	}
	
	with open('example.json','w') as outFile:
		json.dump(exampleDict, outFile, indent=1)
		
	with open('example.json') as inFile:
		exampleDict = json.load(inFile)
	
	print(exampleDict)


if __name__ == '__main__':
	
	NAME, REF, PROF, COMP, PHASES = "name", "refTime", "profTime", "compTime", "phases"
	
# 	testJson()
	benchmarks = []
	
	inFile = open('spec-output-stats/444.namd.clang.scorep.log')
	for line in inFile:
		if "###" in line:
			benchmarkName = line.split()[1]
			d = {PHASES:{}, NAME: benchmarkName}
			benchmarks.append(d)
		if "runtime:" in line:
			d[REF] = line.split()[4]
			d[PROF] = line.split()[1]
		if "new runtime" in line:
			d[COMP] = line.split()[4]
			
		if "==" in line:
			phases = d[PHASES]
			phaseName = line.split('=')[2]
			phases[phaseName] = {}
			phase = phases[phaseName]
			
		if "---->" in line:
			ovPercent = line.split()[1]
			ovSeconds = line.split()[-2]
			phase["percent"] = ovPercent
			phase["seconds"] = ovSeconds
			
	print(benchmarks)
	with open('example.json','w') as outFile:
		json.dump(benchmarks, outFile, indent=1)
	
	