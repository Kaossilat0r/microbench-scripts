# global constants
SAMPLE_PERCENT = 2

NAME, REF, PROF, COMP, PHASES = "name", "refTime", "profTime", "compTime", "phases"
PERCENT, UNW_PERCENT, INSTR_PERCENT = "percent", "unwPercent", "instrPercent"

OUT_DIR = "out-estimate"

PN = {
    'InstrumentAll': 'ss-all',
    'Instrument': 'ss-cpd',
    'MinInstrHeuristic': 'ss-min',
    'ConjInstrHeuristic': 'ss-conj',
    'LibUnwStandard': 'unw-all',
    'LibUnwUnique': 'unw-min',
    'UnwStaticLeaf': 'hybrid-st',
    'UnwindSample': 'hybrid',

    'OvCompensation': '',
    'RemoveUnrelated': '',
    'SanityCheck': '',
    'Reset': ''
}

PHASE_ORDER_INTERNAL = ['InstrumentAll', 'Instrument', 'MinInstrHeuristic', 'ConjInstrHeuristic',
               'LibUnwStandard', 'LibUnwUnique', 'UnwStaticLeaf', 'UnwindSample']

COL = {
    'ss-all': 'violet',
    'ss-cpd': 'blue',
    'ss-min': 'navy',
    'ss-conj': 'purple',
    'unw-all': 'red',
    'unw-min': 'pink',
    'hybrid': 'green',
    'hybrid-st': 'yellow'
}

PHASE_ORDER = []
for name in PHASE_ORDER_INTERNAL:
    PHASE_ORDER.append(PN[name])