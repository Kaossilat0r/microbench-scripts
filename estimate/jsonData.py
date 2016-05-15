"""
Created on 08.05.2016

@author: roman
"""

import json
import glob
from estimate import constants as C


# benchmarks -> phases -> ov-source -> ov-percent/seconds
def parse_benchmark_results(path):
    benchmark_results = []
    for filename in glob.iglob(path + '/*.log'):

        in_file = open(filename)
        for line in in_file:
            if "###" in line:
                benchmark_name = line.split()[1]
                benchmark_name = '.'.join(benchmark_name.split('.')[:2])    # name till second dot
                benchmark = {C.PHASES: {}, C.NAME: benchmark_name}
                benchmark_results.append(benchmark)
                phases = benchmark[C.PHASES]

            if "runtime:" in line:
                benchmark[C.REF] = float(line.split()[4])
                benchmark[C.PROF] = float(line.split()[1])
            if "new runtime" in line:
                benchmark[C.COMP] = float(line.split()[4])

            if "==" in line:
                phase_name = C.PN[line.split('=')[2]]
                if phase_name not in phases:
                    phases[phase_name] = {
                        "percent": 0.0,
                        "seconds": 0.0,
                        "unwPercent": 0.0,
                        "unwSeconds": 0.0,
                        "instrPercent": 0.0,
                        "instrSeconds": 0.0
                    }

            if "---->" in line:
                phase = phases[phase_name]
                ov_percent = float(line.split()[1])
                ov_seconds = float(line.split()[-2])
                phase["percent"] = ov_percent
                phase["seconds"] = ov_seconds

            if "UNW" in line:
                phase = phases[phase_name]
                ov_percent = float(line.split()[1])
                ov_seconds = float(line.split()[-2])
                phase["unwPercent"] = ov_percent
                phase["unwSeconds"] = ov_seconds

            if "INSTR" in line:
                phase = phases[phase_name]
                ov_percent = float(line.split()[1])
                ov_seconds = float(line.split()[-2])
                phase["instrPercent"] = ov_percent
                phase["instrSeconds"] = ov_seconds

    # print(benchmark_results)
    return benchmark_results


def save_file(benchmark_dict, filename):
    with open(filename, 'w') as out_file:
        json.dump(benchmark_dict, out_file, indent=1, sort_keys=True)


def load_file(filename):
    with open(filename) as in_file:
        return json.load(in_file)


if __name__ == '__main__':

    # 	testJson()
    benchmarks = parse_benchmark_results('../spec-output-stats')

    save_file(benchmarks, '../spec-estimations.json')
