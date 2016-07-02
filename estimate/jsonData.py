"""
Created on 08.05.2016

@author: roman
"""

import json
import glob
import os

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
                    phase["percent"] = ov_percent + C.GLOBAL_SAMPLE_PERCENT
                    phase["seconds"] = ov_seconds + C.GLOBAL_SAMPLE_PERCENT * benchmark[C.REF]
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

    benchmark_results = parse_driver_results('../spec-driver-output', benchmark_results)

    benchmark_results_with_avg = benchmark_results.copy()

    # add average values for all benchmarks
    top_level_fields = [C.PROF, C.COMP, C.REF, C.PAPI, C.PAPI_OVERHEAD_PERCENT]
    avg_benchmark = {C.PHASES: {}}
    for field in top_level_fields:
        avg_benchmark[field] = 0.0

    for phase_name, phase in benchmark_results_with_avg["462.libquantum"][C.PHASES].items():
        avg_benchmark[C.PHASES][phase_name] = {}
        for ov_name in ov_names:
            avg_benchmark[C.PHASES][phase_name][ov_name] = 0.0
        if phase_name in C.DRIVER_PHASES:
            avg_benchmark[C.PHASES][phase_name][C.DRIVER_PERCENT] = []

    length = 0
    for benchmark_name, benchmark in benchmark_results_with_avg.items():

        if benchmark_name == '447.dealII':
            continue    # skip this benchmark
        length += 1

        for field in top_level_fields:
            avg_benchmark[field] += benchmark[field]

        for phase_name, phase in benchmark[C.PHASES].items():
            for ov_name, ov_value in phase.items():
                if ov_name != C.DRIVER_PERCENT and ov_name != C.DRIVER_SEC:
                    avg_benchmark[C.PHASES][phase_name][ov_name] += phase[ov_name]
            if phase_name in C.DRIVER_PHASES:
                avg_benchmark[C.PHASES][phase_name][C.DRIVER_PERCENT].append(avg(phase[C.DRIVER_PERCENT]))

    for field in top_level_fields:
        avg_benchmark[field] /= length
    for phase_name, phase in avg_benchmark[C.PHASES].items():
        for ov_name, ov_value in phase.items():
            if ov_name != C.DRIVER_PERCENT and ov_name != C.DRIVER_SEC:
                avg_benchmark[C.PHASES][phase_name][ov_name] /= length
        if phase_name in C.DRIVER_PHASES:
            avg_benchmark[C.PHASES][phase_name][C.DRIVER_PERCENT] = [avg(avg_benchmark[C.PHASES][phase_name][C.DRIVER_PERCENT])]

    benchmark_results_with_avg["average"] = avg_benchmark

    # print(benchmark_results)
    return benchmark_results, benchmark_results_with_avg


def parse_driver_results(path, benchmark_results):

    for filename in glob.iglob(path + '/*_vanilla'):
        cols = os.path.basename(filename).split('_')
        benchmark_name = cols[0]

        if benchmark_name in benchmark_results:
            benchmark_results[benchmark_name][C.REF] = avg(parse_runtimes(filename))

    for filename in glob.iglob(path + '/*_papi'):
        cols = os.path.basename(filename).split('_')
        benchmark_name = cols[0]

        if benchmark_name in benchmark_results:
            runtime_papi = avg(parse_runtimes(filename))
            runtime_ref = benchmark_results[benchmark_name][C.REF]
            benchmark_results[benchmark_name][C.PAPI] = runtime_papi
            benchmark_results[benchmark_name][C.PAPI_OVERHEAD_PERCENT] = (runtime_papi-runtime_ref)/runtime_ref*100.

    for filename in glob.iglob(path + '/*_*-*'):

        cols = os.path.basename(filename).split('_')
        benchmark_name, phase_name = cols[0], cols[1]

        runtime_no_handler = benchmark_results[benchmark_name][C.PAPI]
        runtime_ref = benchmark_results[benchmark_name][C.REF]
        runtime_seconds_data = parse_runtimes(filename)
        overhead_seconds_data = [(x-runtime_ref) for x in runtime_seconds_data]
        benchmark_results[benchmark_name][C.PHASES][phase_name][C.DRIVER_SEC] = overhead_seconds_data
        benchmark_results[benchmark_name][C.PHASES][phase_name][C.DRIVER_PERCENT] = [(x/runtime_ref*100.) for x in overhead_seconds_data]

    return benchmark_results

def avg(list):
    return sum(list) / float(len(list))

def parse_runtimes(filename):
    runtime_seconds_data = []

    in_file = open(filename)
    for line in in_file:
        if "target | " in line:
            runtime = line.split(' ')[8]
            runtime_seconds_data.append(float(runtime))
    return runtime_seconds_data

def save_file(benchmark_dict, filename):
    with open(filename, 'w') as out_file:
        json.dump(benchmark_dict, out_file, indent=1, sort_keys=True)


def load_file(filename):
    with open(filename) as in_file:
        return json.load(in_file)


if __name__ == '__main__':

    # 	testJson()
    benchmarks = parse_benchmark_results('../spec-output-stats')

    parse_driver_results('../spec-driver-output')

    save_file(benchmarks, '../spec-estimations.json')
