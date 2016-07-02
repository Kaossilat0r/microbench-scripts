# global constants
GLOBAL_SAMPLE_PERCENT = 2

NAME, REF, PROF, COMP, PAPI, PHASES = "name", "refTime", "profTime", "compTime", "emptyPapiHandler", "phases"
PERCENT, UNW_PERCENT, INSTR_PERCENT, SAMPLE_PERCENT = "percent", "unwPercent", "instrPercent", "samplePercent"
DRIVER_SEC, DRIVER_PERCENT, PAPI_OVERHEAD_PERCENT = "driverSeconds", "driverPercent", "papiOvPercent"

OUT_DIR = "out-estimate"

PN_DEPRECATED = {
    'InstrumentAll': 'ss-all',
    'Instrument': 'ss-cpd',
    'MinInstrHeuristic': 'ss-min',
    'ConjInstrHeuristic': 'ss-conj',
    'LibUnwStandard': 'unw-all',
    'LibUnwUnique': 'unw-min',
    'UnwStaticLeaf': 'hybrid-st',
    'UnwindSample': 'hybrid-dyn',

    'OvCompensation': '',
    'RemoveUnrelated': '',
    'SanityCheck': '',
    'Reset': ''
}

PN = {
    'ss-all': 'ss-all',
    'ss-cpd': 'ss-cpd',
    'ss-min': 'ss-min',
    'ss-conj': 'ss-conj',
    'unw-all': 'unw-all',
    'unw-min': 'unw-min',
    'hybrid-st': 'hybrid-st',
    'hybrid-dyn': 'hybrid-dyn',

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
    'ss-min': 'purple',
    'ss-conj': 'cyan',
    'unw-all': 'red',
    'unw-min': 'pink',
    'hybrid-dyn': 'green',
    'hybrid-st': 'yellow'
}

DRIVER_PHASES = ["ss-cpd", "ss-min", "unw-all", "unw-min", "hybrid-st", "hybrid-dyn"]

PHASE_ORDER = []
for name in PHASE_ORDER_INTERNAL:
    PHASE_ORDER.append(PN_DEPRECATED[name])