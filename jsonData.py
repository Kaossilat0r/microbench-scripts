"""
Created on 08.05.2016

@author: roman
"""

import json
import glob


# benchmarks -> phases -> ov-source -> ov-percent/seconds
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
                phases[phase_name] = {}

            if "---->" in line:
                phase = phases[phase_name]
                ov_percent = line.split()[1]
                ov_seconds = line.split()[-2]
                phase["percent"] = ov_percent
                phase["seconds"] = ov_seconds

            if "UNW" in line:
                phase = phases[phase_name]
                ov_percent = line.split()[1]
                ov_seconds = line.split()[-2]
                phase["unwPercent"] = ov_percent
                phase["unwSeconds"] = ov_seconds

            if "INSTR" in line:
                phase = phases[phase_name]
                ov_percent = line.split()[1]
                ov_seconds = line.split()[-2]
                phase["instrPercent"] = ov_percent
                phase["instrSeconds"] = ov_seconds

    print(benchmarks)
    return benchmarks


def save_file(filename):
    with open(filename, 'w') as out_file:
        json.dump(benchmarks, out_file, indent=1, sort_keys=True)


def load_file(filename):
    with open(filename) as in_file:
        return json.load(in_file)

# global constants
NAME, REF, PROF, COMP, PHASES = "name", "refTime", "profTime", "compTime", "phases"

if __name__ == '__main__':

    # 	testJson()
    benchmarks = []
    benchmarks = parse_benchmark_results()

    save_file('spec-estimations.json')
