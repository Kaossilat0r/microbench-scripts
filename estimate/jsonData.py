"""
Created on 08.05.2016

@author: roman
"""

import json
import glob
from estimate import constants as C

ov_names = ["seconds", "percent", "unwPercent", "unwSeconds", "instrPercent", "instrSeconds"]

# benchmarks -> phases -> ov-source -> ov-percent/seconds
def parse_benchmark_results(path, consider_sampling_costs=False):
    benchmark_results = {}
    for filename in glob.iglob(path + '/*.log'):

        in_file = open(filename)
        for line in in_file:
            if "###" in line:
                benchmark_name = line.split()[1]
                benchmark_name = '.'.join(benchmark_name.split('.')[:2])    # name till second dot
                benchmark = {C.PHASES: {}}
                benchmark_results[benchmark_name] = benchmark
                phases = benchmark[C.PHASES]

            if "runtime:" in line:
                benchmark[C.REF] = float(line.split()[4])
                benchmark[C.PROF] = float(line.split()[1])
            if "new runtime" in line:
                benchmark[C.COMP] = float(line.split()[4])

            if "==" in line:
                phase_name = C.PN[line.split('=')[2]]
                if phase_name is "":
                    continue

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
                if consider_sampling_costs:
                    phase["percent"] = ov_percent + C.SAMPLE_PERCENT
                    phase["seconds"] = ov_seconds + C.SAMPLE_PERCENT * benchmark[C.REF]
                else:
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

    benchmark_results_with_avg = benchmark_results.copy()

    # add average values for all benchmarks
    avg_benchmark = {C.PHASES: {}, C.PROF: 0.0, C.COMP: 0.0, C.REF: 0.0}
    for phase_name, phase in benchmark_results_with_avg["462.libquantum"][C.PHASES].items():
        avg_benchmark[C.PHASES][phase_name] = {}
        for ov_name in ov_names:
            avg_benchmark[C.PHASES][phase_name][ov_name] = 0.0
    for benchmark in benchmark_results_with_avg.values():
        avg_benchmark[C.REF] += benchmark[C.REF]
        avg_benchmark[C.COMP] += benchmark[C.COMP]
        avg_benchmark[C.PROF] += benchmark[C.PROF]
        for phase_name, phase in benchmark[C.PHASES].items():
            for ov_name, ov_value in phase.items():
                avg_benchmark[C.PHASES][phase_name][ov_name] += phase[ov_name]

    for runtime_name in [C.PROF, C.COMP, C.REF]:
        avg_benchmark[runtime_name] /= len(benchmark_results)
    for phase_name, phase in avg_benchmark[C.PHASES].items():
        for ov_name, ov_value in phase.items():
            avg_benchmark[C.PHASES][phase_name][ov_name] /= len(benchmark_results)

    benchmark_results_with_avg["average"] = avg_benchmark

    # print(benchmark_results)
    return benchmark_results, benchmark_results_with_avg


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
