"""
Created on 08.05.2016

@author: roman
"""

import json
import glob


def test_json():
    example_dict = {
        "astar": {"reftime": 200, "ovComp": 250, "PROF": 500,
                  "phase-instrument": {"instrOv": 20, "sampleOv": 10, "overallOv": 30}},
        "libquantum": {"reftime": 210, "ovComp": 220, "PROF": 700},
    }

    with open('example.json', 'w') as outFile:
        json.dump(example_dict, outFile, indent=1)

    with open('example.json') as inFile:
        example_dict = json.load(inFile)

    print(example_dict)


# benchmarks -> phases -> ovPercent/Seconds
def parse_benchmark_results():

    for filename in glob.iglob('spec-output-stats/*.log'):

        in_file = open(filename)
        for line in in_file:
            if "###" in line:
                benchmark_name = line.split()[1]
                benchmark = {PHASES: {}, NAME: benchmark_name}
                benchmarks.append(benchmark)
                phases = benchmark[PHASES]

            if "runtime:" in line:
                benchmark[REF] = line.split()[4]
                benchmark[PROF] = line.split()[1]
            if "new runtime" in line:
                benchmark[COMP] = line.split()[4]

            if "==" in line:
                phase_name = line.split('=')[2]

            if "---->" in line:
                phase = {}
                ov_percent = line.split()[1]
                ov_seconds = line.split()[-2]
                phase["percent"] = ov_percent
                phase["seconds"] = ov_seconds
                phases[phase_name] = phase

    print(benchmarks)
    return benchmarks


NAME, REF, PROF, COMP, PHASES = "name", "refTime", "profTime", "compTime", "phases"
if __name__ == '__main__':

    # 	testJson()
    benchmarks = []
    benchmarks = parse_benchmark_results()

    with open('example.json', 'w') as outFile:
        json.dump(benchmarks, outFile, indent=1, sort_keys=True)
