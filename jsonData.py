'''
Created on 08.05.2016

@author: roman
'''

import json

def testJson():
	exampleDict = {
		"astar" : {"reftime" : 200, "ovComp" : 250, "profTime" : 500, "phase-instrument" : {"instrOv" : 20, "sampleOv" : 10, "overallOv" : 30} },
		"libquantum" : {"reftime" : 210, "ovComp" : 220, "profTime" : 700},
	}
	
	with open('example.json','w') as outFile:
		json.dump(exampleDict, outFile, indent=1)
		
	with open('example.json') as inFile:
		exampleDict = json.load(inFile)
	
	print(exampleDict)


if __name__ == '__main__':
	
	
# 	testJson()
	
	d = {"phases" :{}}
	phases = d["phases"]
	
	inFile = open('spec-output-stats/444.namd.clang.scorep.log')
	for line in inFile:
		if "###" in line:
			name = line.split()[1]
		if "runtime:" in line:
			d["refTime"] = line.split()[4]
			d["profile"] = line.split()[1]
		if "new runtime" in line:
			d["compTime"] = line.split()[4]
			
		if "==" in line:
			phaseName = line.split('=')[2]
			phases[phaseName] = {}
			
		if "---->" in line:
			ovPercent = line.split()[1]
			ovSeconds = line.split()[-2]
			phases[phaseName]["percent"] = ovPercent
			phases[phaseName]["seconds"] = ovSeconds
			
	print(d)
	with open('example.json','w') as outFile:
		json.dump(d, outFile, indent=1)
	
	